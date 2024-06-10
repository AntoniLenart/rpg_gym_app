from datetime import datetime
from .app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    # badges = db.relationship('Badge', backref='owner', lazy='dynamic')

    def __init__(self, username, email, password_hash, xp=0, level=1):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.xp = xp
        self.level = level


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    rewards = db.Column(db.Integer)
    exercises = db.relationship('Exercise', backref='plan', lazy='dynamic')


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    plan_id = db.Column(db.Integer, db.ForeignKey('workout_plan.id'))
    xp_reward = db.Column(db.Integer)
