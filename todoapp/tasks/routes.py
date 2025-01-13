from flask import Blueprint
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from todoapp.app_init import db
from todoapp.models import Employee, Task
from todoapp.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


@tasks.route('/employer_dashboard')
@login_required
def employer_dashboard():
    employees = Employee.query.filter_by(reference_id=current_user.reference_id).all()

    tasks = []
    for employee in employees:
        tasks.extend(employee.tasks)
        
    return render_template('employer_dashboard.html', tasks=tasks)



@tasks.route('/employer_dashboard/add', methods=['GET', 'POST'])
@login_required
def employer_dashboard_add():
    if current_user.role != 'Employer':
        return redirect(url_for('core.home'))

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
        return redirect(url_for('tasks.employer_dashboard_view'))

    return render_template('employer_dashboard_add.html', form=form)

@tasks.route('/employer_dashboard/view')
@login_required
def employer_dashboard_view():
    if current_user.role != 'Employer':
        return redirect(url_for('core.home'))

    # Fetch all tasks assigned to employees under the employer's reference_id
    employees = Employee.query.filter_by(reference_id=current_user.reference_id).all()
    tasks = []
    for employee in employees:
        tasks.extend(employee.tasks)

    return render_template('employer_dashboard_view.html', tasks=tasks)



@tasks.route('/employee_dashboard')
@login_required
def employee_dashboard():
    # Get the current employee's tasks
    employee_tasks = Task.query.filter_by(employee_id=current_user.id).all()
    return render_template('employee_dashboard.html', tasks=employee_tasks)

@tasks.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Make sure the current user is the one assigned to this task
    if task.employee_id != current_user.id:
        flash('You are not authorized to update this task.', 'danger')
        return redirect(url_for('tasks.employee_dashboard'))
    
    new_status = request.form.get('task_status')
    
    # Update the task status
    task.task_status = new_status
    db.session.commit()
    
    flash('Task status updated successfully!', 'success')
    return redirect(url_for('tasks.employee_dashboard'))


@tasks.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.employee.employer.id != current_user.id:
        flash("You are not authorized to delete this task.", "danger")
        return redirect(url_for('tasks.employer_dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('tasks.employer_dashboard'))