from flask import redirect, url_for, flash
from todoapp.models import Employer, Employee


def get_user_dashboard(user_id):
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