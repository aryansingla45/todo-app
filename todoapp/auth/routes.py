from flask import Blueprint , render_template , url_for , flash , redirect , request
from flask_login import login_user , current_user , logout_user , login_required
from todoapp.app_init import db , bcrypt
from todoapp.models import User , Employer , Employee
from todoapp.auth.forms import LoginForm , Registerform , RequestResetForm , ResetPasswordForm
from todoapp.auth.utils import send_reset_email , get_user_dashboard

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
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

    return render_template('login.html', form=form , title = 'Login')


@auth.route('/register' , methods = ['GET' , 'POST'])
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
            return redirect(url_for('auth.login'))
            
        elif form.role.data == 'Employee':
            employee = Employee(id = user_id , name = form.username.data , reference_id = form.reference_id.data)
            db.session.add(employee)
            db.session.commit()

            flash(f'Your account has been created for {form.role.data}.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f"Erorr in creating account", 'danger')
   
    return render_template('register.html' , form = form)




@auth.route('/forgot' , methods = ['GET' , 'POST'])
def forgot():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        redirect(url_for('auth.login'))
    return render_template('forgot.html' , form = form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.forgot'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.home'))