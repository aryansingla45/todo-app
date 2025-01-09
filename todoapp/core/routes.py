from flask import Blueprint , render_template
from todoapp.core.utils import get_user_dashboard
from flask_login import current_user

core = Blueprint('core', __name__)


@core.route('/')
def home():
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_user_dashboard(user_id)
        
    return render_template('index.html')

@core.route('/about')
def about():
    return render_template('about.html')