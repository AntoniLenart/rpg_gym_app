from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__,
                template_folder='../templates',)
    app.debug = True
    app.config.from_pyfile('../config.py')
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.Config.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints (views)
    from .routes import bp as bp_index
    app.register_blueprint(bp_index)

    return app


if __name__ == '__main__':
    app = create_app()
