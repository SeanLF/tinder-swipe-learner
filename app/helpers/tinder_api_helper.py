# coding=utf-8
'''
Tinder API wrapper
~~~~~~~~~~~~~~~~~

An instance of this class represents a user in the database
'''
from threading import Thread

# from tinder_api import Tinder_API
from ..providers.fake_tinder_api import Tinder_API
import tinder_api.helpers as api_helpers

from ..database.db import get_db
from .db_helper import DB_Helper
from ..models.user import User


class Tinder_API_helper(object):
    def __init__(self, **kwargs):
      self._tinder_api = Tinder_API(**kwargs)


    # Authentication

    def send_sms_otp(self, phone_number):
      return self._tinder_api.send_otp_code(phone_number).get('data').get('sms_sent')


    def get_refresh_token(self, phone_number, otp_code):
      return self._tinder_api.get_refresh_token(phone_number, otp_code) # returns refresh_token

    
    def get_api_token(self, refresh_token):
      return self._tinder_api.get_api_token(refresh_token) # returns api_token


    def get_profile(self):
      return self._tinder_api.get_self()

    
    def get_recommendations(self, limit=5):
      recs = self._tinder_api.get_recs_v2()
      users_dict = recs.get('data', {}).get('results', [])
      users = [User(user) for user in users_dict]

      # in a separate thread, persist users
      DB_Helper().save_users(users)

      return users


    def act_on_user(self, user_id, action):
      response = self._tinder_api.dislike(user_id) if action == 'dislike' else self._tinder_api.like(user_id)

      # in a separate thread, persist action
      t = Thread(target=lambda db_helper, user_id, klass: db_helper.set_user_klass(user_id, klass), args=(DB_Helper(get_db()), user_id, action))
      t.start()

      return response


    def get_matches(self, limit=10, page_token=None):
      response = self._tinder_api.matches(page_token=page_token, limit=limit)
      response_data = response.get('data', {})
      
      matches = response_data.get('matches')
      # matches_for_db = [User(match.get('person')) for match in api_helpers.format_matches(matches)]
      next_page_token = response_data.get('next_page_token', None)


      # in a separate thread, persist users
      DB_Helper() #matches

      # if next_page_token is not None and len(matches) < limit:
      #   missing = limit - len(matches)
      #   matches += self.get_matches(limit=missing, page_token=next_page_token)
      
      return matches, next_page_token


    def get_match_count(self):
      return self._tinder_api.fast_match_count().get('data').get('count')


    def custom_api_call(self, endpoint, http_verb='GET', data={}):
      return self._tinder_api.custom_request(endpoint, http_verb=http_verb, data=data)
