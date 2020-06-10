from flask import Flask
# from flask_restful import Api


def create_app(config_filename=None):
    app = Flask(__name__)

    # app.config.from_pyfile(config_filename)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'doggie-school.sqlite'),
    # )

    if config_filename is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config_filename)

    with app.app_context():
        from .core import app_setup

    return app