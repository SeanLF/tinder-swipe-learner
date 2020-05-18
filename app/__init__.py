import os
from flask import Flask, url_for, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tinder.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import tinder
    app.register_blueprint(tinder.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def index():
        return render_template('index.html', otp_url=url_for('auth.sms_otp_code'), tinder_url=url_for('tinder.index'))

    return app