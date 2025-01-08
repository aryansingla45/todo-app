from todoapp.app_init import app , db , bcrypt
from flask import render_template , flash , redirect , url_for , request
from todoapp.forms import LoginForm , Registerform
from todoapp.models import User , Employer, Employee
from flask_login import login_user , current_user , logout_user , login_required



@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html' , form = form)

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = Registerform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data , password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html' , form = form)

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/myaccount')
@login_required
def myaccount():
    return render_template('myaccount.html')    