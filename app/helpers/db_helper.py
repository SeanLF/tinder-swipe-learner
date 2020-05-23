# coding=utf-8
'''
Use this file to interact with the database. Think of it as an API.
'''

from threading import Thread
from sqlite3 import IntegrityError

from flask import current_app

from ..database.db import get_db
from ..models.user import User

class DB_Helper(object):

    def query_user(self, limit=30, offset=0, likes_me=None, klasses=[]):
      query = self.build_query('SELECT * FROM users', 'LIMIT ? OFFSET ?', likes_me, klasses)
      try:
        users = get_db().execute(query, (limit, offset)).fetchall()
      except IntegrityError as e:
        return str(e)
      return [User(user) for user in users]

    
    def save_users(self, users):
      t = Thread(target=lambda users: map(lambda user: self._save_user(user), users), args=(users))
      t.start()

    
    def _save_user(self, user):
      try:
        get_db().execute(
          'INSERT INTO users (id, photos, age, bio, likes_me, class)'
          ' VALUES (?, ?, ?, ?, ?, ?)',
          (user.id, user.photos_blob(), user.age, user.bio, user.likes_me, user.klass)
        )
        get_db().commit()
      except IntegrityError as e:
        current_app.logger.error("User {id} not saved: {e}".format(id=user.id, e=str(e)))


    def update_users(self, users):
      t = Thread(target=lambda users: map(lambda user: self._update_user(user), users), args=(users))
      t.start()

    
    def _update_user(self, user):
      try:
        get_db().execute(
          'UPDATE users SET id = ?, photos = ?, age = ?, bio = ?, likes_me = ?, class = ?',
          (user.id, user.photos_blob(), user.age, user.bio, user.likes_me, user.klass)
        )
        get_db().commit()
      except IntegrityError as e:
        current_app.logger.error("User {id} not updated: {e}".format(id=user.id, e=str(e)))


    def set_user_klass(self, user_id, klass):
      t = Thread(target=lambda user_id, klass: self._set_user_klass(user_id, klass), args=(user_id, klass))
      t.start()


    def _set_user_klass(self, user_id, klass):
      try:
        get_db().execute(
          'UPDATE users SET class = ? WHERE id = ?',
          (klass, user_id)
        )
        get_db().commit()
      except IntegrityError as e:
        current_app.logger.error("Could not {klass} user {id}: {e}".format(id=user_id, e=str(e)))

      
    def delete_users(self, users):
      t = Thread(target=lambda users: map(lambda user: self._delete_user(user), users), args=(users))
      t.start()


    def _delete_user(self, user):
      try:
        get_db().execute('DELETE FROM users WHERE id = ?', (user.id,))
        get_db().commit()
        del self
      except IntegrityError as e:
        current_app.logger.error("User {id} not deleted: {e}".format(id=user.id, e=str(e)))


    def build_query(self, query, query_end, likes_me, klasses):
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