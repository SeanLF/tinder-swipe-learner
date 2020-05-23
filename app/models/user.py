# coding=utf-8
'''
User
~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of this class represents a user in the database
'''
import json
from sqlite3 import Row

from tinder_api import helpers as api_helpers

from .dot_dict import DotDict

class Match(DotDict):
    pass

class User(DotDict):
    def __init__(self, user):
        if type(user) is Row:
            DotDict.__init__(self,
                id = user['id'],
                name = None,
                age = user['age'],
                distance = None,
                photos = json.loads(user['photos']),
                bio = user['bio'],
                klass = user['klass'],
                match_id = user['match_id'],
            )
        elif type(user) is dict: # API data
            distance = "%i km" % api_helpers.distance_in_km(user.get('distance_mi'))
            user = user.get('user')
            dict.__init__(self,
                distance = distance,
                # photos += [photo['url'] for photo in user['instagram']['photos']] not included anymore,
                id = user.get('id', user.get('_id')),
                name = user.get('name'),
                age = api_helpers.calculate_age(user.get('birth_date')),
                photos = api_helpers.get_photos(user),
                bio = user.get('bio'),
                likes_me = None,
                klass = None,
            )
            
        elif type(user) is Match:
            DotDict.__init__(self, user)


    def photos_to_blob(self):
        return json.dumps(self.photos)

    
    def __getattr__(self, attr):
        return self.get(attr)


    def __setattr__(self, key, value):
        self.__setitem__(key, value)


    def __setitem__(self, key, value):
        super(User, self).__setitem__(key, value)
        self.__dict__.update({key: value})


    def __delattr__(self, item):
        self.__delitem__(item)


    def __delitem__(self, key):
        super(User, self).__delitem__(key)
        del self.__dict__[key]