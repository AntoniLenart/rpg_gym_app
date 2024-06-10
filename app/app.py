from flask import Flask


def create_app():
    app = Flask(__name__,
                template_folder='../templates',)
    app.config.from_pyfile('../configuration.py')
    app.config['SECRET_KEY'] = 'you-will-never-guess'

    # Register blueprints (views)
    from .routes import bp as bp_index
    app.register_blueprint(bp_index)

    return app


if __name__ == '__main__':
    app = create_app()
