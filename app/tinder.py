import json
from datetime import datetime

from flask import Blueprint, g, render_template, request, url_for, jsonify

import tinder_api_sms

from .auth import login_required
from .db import get_db
from sqlite3 import IntegrityError

bp = Blueprint('tinder', __name__, url_prefix='/tinder')

@bp.route('/')
@login_required
def index():
  recs = tinder_api_sms.get_recs_v2()['data']['results']
  persist_tinder_recommendations(recs)
  return render_template('tinder/index.html', profiles=recs, get_age=user_age, match_count = 305, message_count=1, distance=distance_in_km, tinder_action_url=url_for('tinder.action'))

@bp.route('/list')
@login_required
def persisted():
  profiles = get_tinder_recommendations()
  g.total_count = len(profiles)
  return render_template('tinder/list.html', profiles=profiles[0:1], match_count = 305, message_count=1, distance=distance_in_km, tinder_action_url=url_for('tinder.action'), parse_photos=lambda photos: json.loads(photos))

@bp.route('/action', methods=['POST'])
@login_required
def action():
  data = request.get_json()
  id = data['id']
  action = data['action']
  persist_tinder_action(id, action)
  if action == 'dislike':
    return jsonify(tinder_api_sms.dislike(id))
  else:
    return jsonify(tinder_api_sms.like(id))

def user_age(string):
  return datetime.today().year - int(string[0:4])

def distance_in_km(distance):
  MILE_IN_KM = 1.60934
  return int(round(int(distance)*MILE_IN_KM))

def get_tinder_recommendations():
  db = get_db()
  profiles = db.execute(
    'SELECT * FROM users WHERE class is null'
  ).fetchall()

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
    'UPDATE users SET class = ?'
    ' WHERE id = ?',
    (action, id)
  )
  db.commit()
