from flask import Blueprint, render_template, redirect, url_for, flash, request, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user

from .app import db
from .models import User
from .routes import CONFIG
from app.forms import RegistrationForm, LoginForm

import requests
import re


auth = Blueprint('auth', __name__)

PASSWD_PATTERN = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()   
    
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash('Username already taken. Please provide other username.', 'wrong_username')
            return render_template('register.html', form=form)
        
        elif User.query.filter_by(email=form.username.data).first() is not None:
            flash('There is already an account with this e-mail address.', 'wrong_email')
            return render_template('register.html', form=form)
        
        elif form.password.data != form.password2.data:
            flash('Provided passwords do not match.', 'wrong_password')
            return render_template('register.html', form=form)
        
        elif PASSWD_PATTERN.match(form.password.data) is None:
            flash('Your password must be at least 8 characters long, have at least 1 digit, 1 uppercase and 1 lowercase letter.', 'wrong_password')   
            return render_template('register.html', form=form) 
        
        recaptcha_response = request.form.get('g-recaptcha-response')
        data = {
            'secret': CONFIG.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data, xp=0, level=1)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! You can now sign in.', 'registration_success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'wrong_login')
            return render_template('login.html', form=form)
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.profile', username=user.username))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
