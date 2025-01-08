from todoapp.app_init import db , loginmanager
from flask_login import UserMixin


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    # role = db.Column(db.String(60), nullable = False)
    # empolyer_id = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    employer_id = db.Column(db.String(60), nullable = False)