import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash

import config
from .app import db
from app.models import User, WorkoutPlan, Exercise, Badge
from app.forms import LoginForm, RegistrationForm


bp = Blueprint('routes', __name__)

CONFIG = config.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        form = RegistrationForm()
        recaptcha_response = request.form.get('g-recaptcha-response')
        data = {
            'secret': CONFIG.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data,
                        xp=0, level=1)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('routes.login'))
        else:
            flash('Form validation failed. Please check your inputs.', 'danger')
    else:
        flash('Invalid reCAPTCHA. Please try again.', 'danger')
        return redirect(url_for('routes.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('routes.login'))
        print('Login successful')
        return redirect(url_for('routes.index'))
    return render_template('login.html', form=form)


@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
