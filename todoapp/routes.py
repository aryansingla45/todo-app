from todoapp.app_init import app , db , bcrypt  , mail
from flask import render_template , flash , redirect , url_for , request
from todoapp.forms import LoginForm , Registerform , TaskForm , AccountUpdateForm , RequestResetForm , ResetPasswordForm
from todoapp.models import User , Employer, Employee, Task
from flask_login import login_user , current_user , logout_user , login_required
from todoapp.utils import get_user_dashboard , save_picture , send_reset_email
from flask_mail import Message


@app.route('/')
def home():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
        
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                user_id = user.id
                return get_user_dashboard(user_id)

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form)



@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
    form = Registerform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data , password = hashed_password , 
                    role = form.role.data , reference_id = form.reference_id.data)
        db.session.add(user)
        db.session.commit()

        user_id = user.id

        if form.role.data == 'Employer':
            employer = Employer(id = user_id, name = form.username.data , reference_id = form.reference_id.data)
            db.session.add(employer)
            db.session.commit()

            flash(f'Your account has been created for {form.role.data}.', 'success')
            return redirect(url_for('login'))
            
        elif form.role.data == 'Employee':
            employee = Employee(id = user_id , name = form.username.data , reference_id = form.reference_id.data)
            db.session.add(employee)
            db.session.commit()

            flash(f'Your account has been created for {form.role.data}.', 'success')
            return redirect(url_for('login'))
        else:
            flash(f"Erorr in creating account", 'danger')
   
    return render_template('register.html' , form = form)

    
@app.route('/forgot' , methods = ['GET' , 'POST'])
def forgot():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        redirect(url_for('login'))
    return render_template('forgot.html' , form = form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/employer_dashboard')
@login_required
def employer_dashboard():
    employees = Employee.query.filter_by(reference_id=current_user.reference_id).all()

    tasks = []
    for employee in employees:
        tasks.extend(employee.tasks)
    
    return render_template('employer_dashboard.html', tasks=tasks)



@app.route('/employer_dashboard/add', methods=['GET', 'POST'])
@login_required
def employer_dashboard_add():
    if current_user.role != 'Employer':
        return redirect(url_for('home'))

    form = TaskForm()

    # Populate employee choices based on the employer
    form.employee.choices = [(e.id, e.name) for e in Employee.query.filter_by(reference_id=current_user.reference_id).all()]
    
    if form.validate_on_submit():
        task = Task(
            task_name=form.task_name.data,
            task_description=form.task_description.data,
            task_status=form.task_status.data,
            employee_id=form.employee.data,
            task_deadline=form.task_deadline.data
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task has been added successfully!', 'success')
        return redirect(url_for('employer_dashboard_view'))

    return render_template('employer_dashboard_add.html', form=form)

@app.route('/employer_dashboard/view')
@login_required
def employer_dashboard_view():
    if current_user.role != 'Employer':
        return redirect(url_for('home'))

    # Fetch all tasks assigned to employees under the employer's reference_id
    employees = Employee.query.filter_by(reference_id=current_user.reference_id).all()
    tasks = []
    for employee in employees:
        tasks.extend(employee.tasks)

    return render_template('employer_dashboard_view.html', tasks=tasks)



@app.route('/employee_dashboard')
@login_required
def employee_dashboard():
    # Get the current employee's tasks
    employee_tasks = Task.query.filter_by(employee_id=current_user.id).all()
    return render_template('employee_dashboard.html', tasks=employee_tasks)

@app.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Make sure the current user is the one assigned to this task
    if task.employee_id != current_user.id:
        flash('You are not authorized to update this task.', 'danger')
        return redirect(url_for('employee_dashboard'))
    
    new_status = request.form.get('task_status')
    
    # Update the task status
    task.task_status = new_status
    db.session.commit()
    
    flash('Task status updated successfully!', 'success')
    return redirect(url_for('employee_dashboard'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/myaccount', methods=['GET'])
@login_required
def myaccount():
    return render_template('myaccount.html')


@app.route("/account/update", methods=['GET', 'POST'])
@login_required
def accountupdate():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('myaccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Show the current profile image if available
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account_update.html', title='Account', image_file=image_file, form=form)








@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.employee.employer.id != current_user.id:
        flash("You are not authorized to delete this task.", "danger")
        return redirect(url_for('employer_dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('employer_dashboard'))

