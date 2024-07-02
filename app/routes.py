from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, Rank

import config

bp = Blueprint('routes', __name__)

CONFIG = config.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    print(User.query.filter_by(username='Bruno69').first())
    return render_template('index.html')


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    current_user.get_stats().xp = 20
    return render_template('profile.html', user=current_user)
