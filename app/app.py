from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import config

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__,
                template_folder='../templates', )
    app.debug = True
    app.config.from_pyfile('../config.py')
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/gym_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.Config.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    with app.app_context():
        db.create_all()

    # Register blueprints (views)
    from .routes import bp as bp_index
    app.register_blueprint(bp_index)
    from .auth import auth as bp_auth
    app.register_blueprint(bp_auth)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


if __name__ == '__main__':
    app = create_app()
