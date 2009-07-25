# -*- coding: utf-8 -*-
from google.appengine.ext import db
from Crypto.Cipher import XOR
from Crypto.Hash import MD5

class CipherProperty(db.Property):
    data_type = basestring
    
    def __get__(self, model_instance, model_class):
        value = super(CipherProperty, self).__get__(model_instance, model_class)
        if isinstance(value, db.Blob):
            value = unicode(XOR.new(MD5.new(self.model_class.kind()).digest()).decrypt(value))
            super(CipherProperty, self).__set__(model_instance, value)
        elif isinstance(value, basestring):
            value = unicode(value)
        return value
    
    def get_value_for_datastore(self, model_instance):
        value = super(CipherProperty, self).get_value_for_datastore(model_instance)
        if isinstance(value, basestring):
            value = db.Blob(XOR.new(MD5.new(self.model_class.kind()).digest()).encrypt(value))
        elif isinstance(value, db.Blob):
            value = db.Blob(value)
        return value
