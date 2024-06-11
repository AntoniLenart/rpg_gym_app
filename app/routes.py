from flask import Blueprint, render_template, redirect, url_for, request, flash

import config
from app.models import User, WorkoutPlan, Exercise, Badge


bp = Blueprint('routes', __name__)

CONFIG = config.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
