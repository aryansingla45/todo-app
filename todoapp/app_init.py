from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '4d8s1127df7df484d8fsd484d8f4'
app.config['SALT'] = '4d8s1127df7df484d45s18s81ds77778a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp_database'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'auth.login'

migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'todo.webapp6@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

print(app.config['MAIL_PASSWORD'])

mail = Mail(app)

# Import routes after app initialization
from todoapp.auth.routes import auth
from todoapp.core.routes import core
from todoapp.user_management.routes import user_management
from todoapp.tasks.routes import tasks


app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(user_management)
app.register_blueprint(tasks)
