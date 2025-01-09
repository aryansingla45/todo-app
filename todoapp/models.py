from todoapp.app_init import db, loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(60), nullable=False)
    reference_id = db.Column(db.String(10), nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    reference_id = db.Column(db.String(10), unique=True, nullable=False)  # Unique for each employer

    employees = db.relationship('Employee', backref='employer', lazy=True)

    def __repr__(self):
        return f"Employer('{self.name}')"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    reference_id = db.Column(db.String(10), db.ForeignKey('employer.reference_id'), nullable=False)  # Reference to Employer's reference_id

    tasks = db.relationship('Task', backref='employee', lazy=True)

    def __repr__(self):
        return f"Employee('{self.name} - {self.reference_id}')"


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(40), nullable=False)
    task_description = db.Column(db.String(200), nullable=False)
    task_status = db.Column(db.String(20), nullable=False)
    task_deadline = db.Column(db.Date, nullable=True)  # Add the task deadline field

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.task_name}', '{self.task_status}', '{self.task_deadline}')"
    
    def update_status(self, status):
        self.task_status = status
        db.session.commit()

