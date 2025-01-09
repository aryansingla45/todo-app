from flask import url_for , redirect , flash
from flask_mail import Message
from todoapp.models import Employer, Employee
from todoapp.app_init import mail



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender= "noreply@todo-flaskapp.com", recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}
 If you did not make this request, simply ignore this email and no changes will be made.'''
    mail.send(msg)


def get_user_dashboard(user_id):
    # Check if the user is an Employer
    employer = Employer.query.filter_by(id=user_id).first()
    if employer:
        return redirect(url_for('tasks.employer_dashboard'))

    # Check if the user is an Employee
    employee = Employee.query.filter_by(id=user_id).first()
    if employee:
        return redirect(url_for('tasks.employee_dashboard'))

    # If neither is found (error handling)
    flash('User role is undefined or invalid.', 'danger')
    return redirect(url_for('auth.login'))