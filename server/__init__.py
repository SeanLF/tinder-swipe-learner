import os
from flask import Flask, url_for, render_template, redirect, g
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_ENV='development',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    CORS(app, resources={r'/*': {'origins': '*'}})

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from server.controllers import auth
    app.register_blueprint(auth.bp)

    from server.controllers import tinder
    app.register_blueprint(tinder.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    @auth.login_required
    def index():
        auth.refresh_api_token()
        return redirect(url_for('tinder.index'))

    return app
