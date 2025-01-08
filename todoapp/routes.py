from todoapp.app_init import app , db , bcrypt
from flask import render_template , flash , redirect , url_for , request
from todoapp.forms import LoginForm , Registerform
from todoapp.models import User , Employer, Employee
from flask_login import login_user , current_user , logout_user , login_required
from todoapp.utils import get_user_dashboard


@app.route('/')
def home():
    if current_user.is_authenticated:
        user_id = current_user.id
        
        # Check if the user is an Employer
        employer = Employer.query.filter_by(id=user_id).first()
        if employer:
            return redirect(url_for('dashboard_employer'))

        # Check if the user is an Employee
        employee = Employee.query.filter_by(id=user_id).first()
        if employee:
            return redirect(url_for('dashboard_employee'))
        
        # If neither is found (error handling)
        flash('User role is undefined or invalid.', 'danger')
        return redirect(url_for('login'))
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
        return redirect(url_for('dashboard'))
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







    
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/dashboard_employer')
@login_required
def dashboard_employer():
    return render_template('dashboard_employer.html')

@app.route('/dashboard_employee')
@login_required
def dashboard_employee():
    return render_template('dashboard_employee.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/myaccount')
@login_required
def myaccount():
    return render_template('myaccount.html')    