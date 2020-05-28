import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from server.helpers import Tinder_API_helper

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
    
    CORS(app, resources={r'/*': {'origins': '*'}}, expose_headers='X-Auth-Token')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    tinder_bp = Blueprint('tinder', __name__, url_prefix='/tinder')

    # --------- AUTH ---------

    @tinder_bp.route('/login/sms', methods=['POST'])
    def sms_login():
        data = request.get_json()
        return jsonify(Tinder_API_helper().send_sms_otp(data['phone_number']))

    @tinder_bp.route('/login/sms/otp', methods=['POST'])
    def sms_otp_code():
        data = request.get_json()
        api_helper = Tinder_API_helper()
        # if code present, then user logging in, else only get new tinder token
        if 'otp_code' in data:
            phone_number = data['phone_number']
            otp_code = data['otp_code']
            refresh_api_token = api_helper.get_refresh_token(phone_number, otp_code)
        elif 'refresh_api_token' in data:
            refresh_api_token = data['refresh_api_token']
        api_token = api_helper.get_api_token(refresh_api_token)
        return jsonify({'refresh_token': refresh_api_token, 'api_token': api_token})

    # -------- API --------

    def api_helper():
        return Tinder_API_helper(api_token=request.headers.get('X-Auth-Token'))

    @tinder_bp.route('/recommendations', methods=['GET'])
    def next_profile():
        return jsonify(api_helper().get_recommendations())

    @tinder_bp.route('/profile')
    def profile():
        return jsonify(api_helper().get_profile())

    @tinder_bp.route('/matches', methods=['GET'])
    def get_matches():
        page_token = request.args.get('pageToken', None)
        limit = int(request.args.get('limit', 10))
        return jsonify(api_helper().get_matches(limit=limit, page_token=page_token))

    @tinder_bp.route('/swipe', methods=['POST'])
    def swipe():
        data = request.get_json()
        return jsonify(api_helper().act_on_user(data['id'], data['action']))

    app.register_blueprint(tinder_bp)

    return app
