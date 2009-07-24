# -*- coding: utf-8 -*-
from google.appengine.ext import db
from Crypto.Cipher import XOR
from Crypto.Hash import MD5

class CipherProperty(db.Property):
    data_type = basestring
    
    def get_value_for_datastore(self, model_instance):
        value = super(CipherProperty, self).get_value_for_datastore(model_instance)
        if isinstance(value, basestring) or isinstance(value, db.Text):
            return db.Blob(XOR.new(MD5.new(self.model_class.kind()).digest()).encrypt(value))
        elif isinstance(value, db.Blob):
            return db.Blob(value)
    
    def make_value_from_datastore(self, value):
        value = super(CipherProperty, self).make_value_from_datastore(value)
        if isinstance(value, db.Blob):
            return unicode(XOR.new(MD5.new(self.model_class.kind()).digest()).decrypt(value))
        elif isinstance(value, basestring) or isinstance(value, db.Text):
            return unicode(value)
