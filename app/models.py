from datetime import datetime
from .app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    # badges = db.relationship('Badge', backref='owner', lazy='dynamic')


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
