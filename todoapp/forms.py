from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField , SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from todoapp.models import User, Employer , Employee


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
        # Check if the role is Employer and if the reference_id is already taken in the Employer table
        if self.role.data == 'Employer':
            employer = Employer.query.filter_by(reference_id=reference_id.data).first()
            if employer:
                raise ValidationError('That reference ID is already taken by another employer. Please choose a different one.')

        # Check if the reference_id exists for an Employee or User
        user = User.query.filter_by(reference_id=reference_id.data).first()
        if user:
            if self.role.data == 'Employee':
                # Allow multiple employees with the same reference_id (no problem)
                return
            
            # For other roles, raise validation error if reference_id exists
            raise ValidationError('This reference ID is already taken. Please choose a different one.')

        

        


