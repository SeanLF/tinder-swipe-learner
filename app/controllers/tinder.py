import json
from datetime import datetime

from flask import Blueprint, g, render_template, request, url_for, jsonify

from auth import login_required
from helpers.tinder_api import Tinder_API_helper
from models.user import User

bp = Blueprint('tinder', __name__, url_prefix='/tinder')

api_helper = Tinder_API_helper()


@bp.route('/')
@login_required
def index():
  g.profile = api_helper.get_recommendations()
  load_globals()
  return render_template('tinder/index.html', tinder_action_url=url_for('tinder.action'), tinder_fetch_profile_url=url_for('tinder.next_profile'))


@bp.route('/recommendations', methods=['GET'])
@login_required
def next_profile():
  likes_me = 'likes_me' in request.args
  persisted = 'persisted' in request.args
  limit = int(request.args.get('limit', 10))
  offset = int(request.args.get('offset', 0))

  if persisted or likes_me:
    return jsonify(User.query(limit=limit, offset=offset, likes_me=likes_me))

  users = api_helper.get_recommendations(limit=limit)[0:limit]
  return jsonify(users)


@login_required
def load_globals():
  g.match_count = api_helper.get_match_count()
  g.message_count = 1
  my_profile = api_helper.get_self()
  g.user_profile = {
    'id': my_profile['_id'],
    'name': my_profile['name'],
    'photo': my_profile['photos'][0]['processedFiles'][3]
  }


@bp.route('/matches', methods=['GET'])
@login_required
def get_matches():
  page_token = request.args.get('next_page_token', None)
  limit = request.args.get('limit', 10)
  return jsonify(api_helper.get_matches(limit=limit, page_token=page_token))


@bp.route('/action', methods=['POST'])
@login_required
def action():
  data = request.get_json()
  return jsonify(api_helper.act_on_user(data['id'], data['action']))


@bp.route('/action/custom', methods=['GET', 'POST'])
@login_required
def custom_action():
  http_verb = request.method
  if http_verb == 'GET':
    data = request.args.copy()
    endpoint = data['endpoint']
  else:
    data = request.json()
    endpoint = data['endpoint']
    del data['endpoint']

  return jsonify(api_helper.custom_api_call(endpoint, http_verb=http_verb, data=data))
