from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField , BooleanField , SelectField , TextAreaField , DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError  
from flask_login import current_user
from todoapp.models import User, Employer


class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=3, max=40)])
    task_description = TextAreaField('Task Description', validators=[DataRequired(), Length(min=10, max=200)])
    employee = SelectField('Assign to Employee', coerce=int, validators=[DataRequired()])
    task_deadline = DateField('Task Deadline', validators=[DataRequired()])
    task_status = SelectField('Task Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    submit = SubmitField('Add Task')


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
    

class Registerform(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email' , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , validators=[DataRequired() , Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Employer', 'Employer'), ('Employee', 'Employee')], validators=[DataRequired()])
    reference_id = StringField('Reference ID' , validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.') 
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please log in.')
        
    

    def validate_reference_id(self, reference_id):
        if self.role.data == 'Employer':
            employer = Employer.query.filter_by(reference_id=reference_id.data).first()
            if employer:
                raise ValidationError('That reference ID is already taken by another employer. Please choose a different one.')

        user = User.query.filter_by(reference_id=reference_id.data).first()
        if user:
            if self.role.data == 'Employee':
                return
            
            raise ValidationError('This reference ID is already taken. Please choose a different one.')
        

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

        

        


