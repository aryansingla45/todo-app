from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=3, max=40)])
    task_description = TextAreaField('Task Description', validators=[DataRequired(), Length(min=10, max=200)])
    employee = SelectField('Assign to Employee', coerce=int, validators=[DataRequired()])
    task_deadline = DateField('Task Deadline', validators=[DataRequired()])
    task_status = SelectField('Task Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    submit = SubmitField('Add Task')