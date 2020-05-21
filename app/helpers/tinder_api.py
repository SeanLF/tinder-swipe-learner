# coding=utf-8
'''
Tinder API wrapper
~~~~~~~~~~~~~~~~~

An instance of this class represents a user in the database
'''
from flask import g

from models.user import User


class Tinder_API_helper(object):
    def __init__(self):
      from tinder_api import Tinder_API
      self._tinder_api = Tinder_API(api_token=g.api_token)


    def get_profile(self):
      return self._tinder_api.get_self()

    
    def get_recommendations(self, limit=5):
      recs = self._tinder_api.get_recs_v2()
      users_dict = recs.get('data', {}).get('results', [])
      users = [User(user) for user in users_dict]

      # in a separate thread, persist users
      from threading import Thread
      t = Thread(target=lambda users: map(lambda user: user.save()), args=(users))
      t.start()

      return users


    def act_on_user(self, user_id, action):
      response = self._tinder_api.dislike(id) if action == 'dislike' else self._tinder_api.like(id)

      # in a separate thread, persist action
      from threading import Thread
      t = Thread(target=lambda User, id, klass: User.set_klass(id, klass), args=(User, user_id, action))
      t.start()

      return response


    def get_matches(self, limit=10, page_token=None):
      response = self._tinder_api.matches(page_token=page_token) #, limit=limit)
      response_data = response.get('data', {})
      
      matches = response_data.get('matches')
      next_page_token = response_data.get('next_page_token', None)

      # in a separate thread, persist users
      from threading import Thread
      t = Thread(target=lambda User, matches: map(lambda match: User(match.get('person').save())), args=(User, matches))
      t.start()

      if next_page_token is not None and len(matches) < limit:
        missing = limit - len(matches)
        matches += self.get_matches(limit=missing, page_token=next_page_token) #, limit=limit))
      
      return matches, next_page_token


    def get_match_count(self):
      return self._tinder_api.fast_match_count()


    def custom_api_call(self, endpoint, http_verb='GET', data={}):
      return self._tinder_api.custom_request(endpoint, http_verb=http_verb, data=data)