from flask import redirect, url_for, flash
from todoapp.models import Employer, Employee
import os , secrets
from todoapp.app_init import app
from PIL import Image


def get_user_dashboard(user_id):
    # Check if the user is an Employer
    employer = Employer.query.filter_by(id=user_id).first()
    if employer:
        return redirect(url_for('employer_dashboard'))

    # Check if the user is an Employee
    employee = Employee.query.filter_by(id=user_id).first()
    if employee:
        return redirect(url_for('employee_dashboard'))

    # If neither is found (error handling)
    flash('User role is undefined or invalid.', 'danger')
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn