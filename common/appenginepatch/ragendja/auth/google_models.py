from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from google.appengine.api import users
from google.appengine.ext import db
from django.contrib.auth.models import DjangoCompatibleUser

class GoogleUserTraits(DjangoCompatibleUser):
    @classmethod
    def get_djangouser_for_user(cls, user):
        django_user = cls.get_by_key_name(str(user.user_id()))
        
        if not django_user:
            django_user = cls.create_djangouser_for_user(user)
            django_user.put()
            
        return django_user

    class Meta:
        abstract = True

class User(GoogleUserTraits):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @classmethod
    def create_djangouser_for_user(cls, user):
        return cls(key_name=str(user.user_id()), username=user.nickname().split('@', 1)[0], email=user.email())
