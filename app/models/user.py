# coding=utf-8
'''
User
~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of this class represents a user in the database
'''
import json
from sqlite3 import IntegrityError, Row

from tinder_api import helpers as api_helpers

from database import db


# persist_tinder_profiles(profiles, likes_me=False)
# ->
# User(profile['_id'], profile['photos'], get_age(profile['birth_date']), profile['bio'], None, None)

# persist_tinder_action(id, action)
# ->
# User.set_klass(id, action)

class User(object):
    def __init__(self, user):
      if type(user) is Row:
        self.id = user['id']
        self.name = None
        self.age = user['age']
        self.distance = None
        self.photos = json.loads(user['photos'])
        self.bio = user['bio']
        self.likes_me = user['likes_me']
        self.klass = user['klass']
      elif type(user) is dict: # API data
        self.id = user.get('id', user.get('_id'))
        self.name = user.get('name')
        self.age = api_helpers.calculate_age(user.get('birth_date'))
        self.distance = "%i km" % api_helpers.distance_in_km(user.get('distance_mi'))
        self.photos = api_helpers.get_photos(user)
        self.bio = user.get('bio')
        self.likes_me = None
        self.klass = None


    @classmethod
    def query(cls, limit=30, offset=0, likes_me=None, klasses=[]):
      query = cls.build_query('SELECT * FROM users', 'LIMIT ? OFFSET ?', likes_me, klasses)
      try:
        users = db.execute(query, (limit, offset)).fetchall()
      except IntegrityError as e:
        return str(e)
      return [cls(user) for user in users]

    
    def save(self):
      try:
        db.execute(
          'INSERT INTO users (id, photos, age, bio, likes_me, class)'
          ' VALUES (?, ?, ?, ?, ?, ?)',
          (self.id, self.photos_blob(), self.age, self.bio, self.likes_me, self.klass)
        )
        db.commit()
      except IntegrityError as e:
        return str(e)
      return True

    
    def update(self):
      try:
        db.execute(
          'UPDATE users SET id = ?, photos = ?, age = ?, bio = ?, likes_me = ?, class = ?',
          (self.id, self.photos_blob(), self.age, self.bio, self.likes_me, self.klass)
        )
        db.commit()
      except IntegrityError as e:
        return str(e)
      return True

    
    @classmethod
    def set_klass(cls, id, klass):
      try:
        db.execute('UPDATE users SET class = ? WHERE id = ?', (klass, id))
        db.commit()
      except IntegrityError as e:
        return str(e)
      return True


    def delete(self):
      try:
        db.execute('DELETE FROM users WHERE id = ?', (self.id,))
        db.commit()
      except IntegrityError as e:
        return str(e)
      del self
      return True

    
    def photos_blob(self):
      return json.dumps(self.photos)


    @classmethod
    def blob_to_photos(cls, photos):
      return json.loads(photos)

    
    @classmethod
    def build_query(cls, query, query_end, likes_me, klasses):
      where_clause = []
      if likes_me is not None:
        where_clause.append('likes_me IS TRUE')
      if classes != []:
        permitted_classes = {'like': '"like"', 'superlike': '"superlike"', 'dislike': '"dislike"', None: '"NULL"'}
        classes = [permitted_classes[klass] for klass in klasses]
        where_clause.append("class IN (%s)" % ', '.join(classes))
      if where_clause != []:
        query = ' WHERE '.join([query, ' AND '.join(where_clause)])
      query = ' '.join([query, query_end])
      return query
