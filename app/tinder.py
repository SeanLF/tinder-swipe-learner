import json
from datetime import datetime

from flask import Blueprint, g, render_template, request, url_for, jsonify

# import tinder_api
import app.tinder_api as tinder_api

from .auth import login_required
from .db import get_db
from sqlite3 import IntegrityError

bp = Blueprint('tinder', __name__, url_prefix='/tinder')

@bp.route('/')
@login_required
def index():
  g.profile = view_model_profile(get_tinder_recommendations(limit=1)[0])
  load_globals()
  return render_template('tinder/index.html', tinder_action_url=url_for('tinder.action'), tinder_fetch_profile_url=url_for('tinder.next_profile'))

@bp.route('/next_profile', methods=['GET'])
@login_required
def next_profile():
  profile = get_tinder_recommendations(limit=1)[0]
  return jsonify(view_model_profile(profile))

def load_globals():
  g.match_count = json.loads(tinder_api.fast_match_info())
  g.message_count = 1
  my_profile = tinder_api.get_self()
  g.user_profile = {
    'id': my_profile['_id'],
    'name': my_profile['name'],
    'photo': my_profile['photos'][0]['processedFiles'][3]
  }

@bp.route('/matches', methods=['GET'])
@login_required
def matches():
  page_token = request.args.get('next_page_token')
  matches = tinder_api.matches(page_token=page_token)
  return jsonify(matches)

@bp.route('/action', methods=['POST'])
@login_required
def action():
  data = request.get_json()
  id = data['id']
  action = data['action']
  persist_tinder_action(id, action)
  if action == 'dislike':
    return jsonify(tinder_api.dislike(id))
  else:
    return jsonify(tinder_api.like(id))

def user_age(string):
  return datetime.today().year - int(string[0:4])

def distance_in_km(distance):
  MILE_IN_KM = 1.60934
  return int(round(int(distance)*MILE_IN_KM))

def get_tinder_recommendations(limit=30):
  db = get_db()
  profiles = db.execute('SELECT * FROM users WHERE class IS NULL LIMIT ?', (str(limit))).fetchall()
  if len(profiles) == 0:
    # fetch more
    profiles = tinder_api.get_recs_v2()['data']['results']
    persist_tinder_recommendations(profiles)
    get_tinder_recommendations(limit=limit)
  return profiles

def persist_tinder_recommendations(profiles):
  db = get_db()
  for profile in profiles:
    id = profile['user']['_id']
    photos = [photo['url'] for photo in profile['user']['photos']]
    age = user_age(profile['user']['birth_date'])
    bio = profile['user']['bio']

    if 'instagram' in profile:
      if 'photos' in profile['instagram']:
        for image in profile['instagram']['photos']:
          photos.append(image['image'])
    try:
      db.execute(
        'INSERT INTO users (id, photos, age, bio)'
        ' VALUES (?, ?, ?, ?)',
        (id, json.dumps(photos), age, bio)
      )
      db.commit()
    except IntegrityError:
      continue

def persist_tinder_action(id, action):
  db = get_db()
  db.execute(
    'UPDATE users SET class = ? WHERE id = ?',
    (action, id)
  )
  db.commit()

def parse_images(images):
  return json.loads(images)

def view_model_profile(profile):
  if type(profile) is dict: # data from API
    return {
      'id': profile['id'],
      'name': profile['user']['name'],
      'age': user_age(profile['user']['birth_date']),
      'distance': f"{distance_in_km(profile['distance_mi'])} km",
      'photos': [photo['url'] for photo in profile['user']['photos']],
      'bio': profile['user']['bio'],
      'instagram': {
        'photos': [photo['thumbnail'] for photo in profile['instagram']['photos']]
      }
    }
  else: # data from DB
    return {
      'id': profile['id'],
      'name': '',
      'age': profile['age'],
      'distance': '',
      'photos': json.loads(profile['photos']),
      'bio': profile['bio'],
      'instagram': {
        'photos': []
      }
    }