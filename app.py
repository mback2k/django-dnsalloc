import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import users
from handlers import home, dashboard, admin, log, feedrss

class Login(webapp.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url('https://dnsalloc.appspot.com/'))
        else:
            self.redirect('/')

class Logout(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url('http://dnsalloc.appspot.com/'))
        else:
            self.redirect('/')

ROUTES = [
    ('/', home.Handler),
    ('/feed/([a-z]+)/(.*)/', feedrss.Handler),
    ('/dashboard/([a-z]+)/(.+)/', dashboard.Handler),
    ('/dashboard/', dashboard.Handler),
    ('/admin/([a-z]+)/([0-9]+)/', admin.Handler),
    ('/admin/', admin.Handler),
    ('/log/', log.Handler),
    ('/login/', Login),
    ('/logout/', Logout)
]

def main():
    webapp.template.register_template_library('utils.datetimefilters')
    application = webapp.WSGIApplication(ROUTES)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
