from .app import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    stats = db.relationship('Statistics', backref='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'User {self.username}'

    def get_stats(self):
        return self.stats[0]

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Statistics(db.Model):
    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    xp = db.Column(db.Integer, nullable=False, default=0)
    next_level_xp = db.Column(db.Integer)
    level = db.Column(db.Integer, nullable=False, default=1)
    title = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'{self.user.username}\'s stats'

class Rank(db.Model):
    __tablename__ = 'ranks'

    level = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    required_xp = db.Column(db.Integer, nullable=False)