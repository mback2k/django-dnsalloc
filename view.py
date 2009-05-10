import datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template

def render(request, template_path, template_page, template_dict={}):
    template_dict['page'] = template_page
    template_dict['root'] = users.is_current_user_admin()
    template_dict['user'] = users.get_current_user()
    template_dict['time'] = datetime.datetime.now()
    template_dict['mobi'] = 'Mobile/' in request.headers['User-Agent']
    return template.render(template_path, template_dict)
