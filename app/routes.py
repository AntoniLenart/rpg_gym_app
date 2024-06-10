import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash

import configuration
from app import db
from app.models import User, WorkoutPlan, Exercise, Badge
from app.forms import LoginForm, RegistrationForm


bp = Blueprint('routes', __name__)

CONFIG = configuration.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        data = {
            'secret': CONFIG.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            if form.validate_on_submit():
                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('routes.login'))
            else:
                flash('Form validation failed. Please check your inputs.', 'danger')
        else:
            flash('Invalid reCAPTCHA. Please try again.', 'danger')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('routes.login'))
        return redirect(url_for('routes.index'))
    return render_template('login.html', form=form)


@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
