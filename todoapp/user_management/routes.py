from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from todoapp.app_init import db
from todoapp.models import User
from todoapp.user_management.forms import AccountUpdateForm
from todoapp.user_management.utils import save_picture

user_management = Blueprint('user_management', __name__)



@user_management.route('/myaccount', methods=['GET'])
@login_required
def myaccount():
    return render_template('myaccount.html')


@user_management.route("/account/update", methods=['GET', 'POST'])
@login_required
def accountupdate():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_management.myaccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Show the current profile image if available
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account_update.html', title='Account', image_file=image_file, form=form)