from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,
                template_folder='../templates', )
    app.debug = True
    app.config.update(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess',
        RECAPTCHA_SECRET_KEY = '6LckD6EfAAAAAEHzq9XhuBlj_tutx-PlA-KNDa3Q',
        RECAPTCHA_PUBLIC_KEY = '6LckD6EfAAAAAKqk5lcYli_Get0k-ZzNQxADIA4q',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/rpg_gym_app',
    )

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    with app.app_context():
        db.create_all()

    from .routes import bp as bp_index
    app.register_blueprint(bp_index)
    from .auth import auth as bp_auth
    app.register_blueprint(bp_auth)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

if __name__ == '__main__':
    app = create_app()
