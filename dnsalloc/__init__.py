# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import users

if not '_get_value_for_datastore' in db.UserProperty.__dict__:
    db.UserProperty._get_value_for_datastore = db.UserProperty.get_value_for_datastore

if not '_make_value_from_datastore' in db.UserProperty.__dict__:
    db.UserProperty._make_value_from_datastore = db.UserProperty.make_value_from_datastore

class User(db.Model):
    user = db.StringProperty()

def get_value_for_datastore(self, model_instance):
    model_instance = self._get_value_for_datastore(model_instance)
    if isinstance(model_instance, users.User):
        return User.get_or_insert('user%s' % model_instance.user_id(), user=model_instance.email()).key()
    return None

def make_value_from_datastore(self, value):
    if isinstance(value, db.Key):
        return users.User(email=User.get(value).user)
    return self._make_value_from_datastore(value)

db.UserProperty.get_value_for_datastore = get_value_for_datastore
db.UserProperty.make_value_from_datastore = make_value_from_datastore
