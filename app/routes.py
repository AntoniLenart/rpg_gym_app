from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import User, WorkoutPlan, Exercise, Badge

import config

bp = Blueprint('routes', __name__)

CONFIG = config.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    print(User.query.filter_by(username='Bruno69').first())
    return render_template('index.html')


@bp.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
