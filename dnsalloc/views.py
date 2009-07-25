import datetime
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from dnsalloc.forms import ServiceForm
from dnsalloc.feeds import ResultFeed
from dnsalloc.models import Service, Result
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404
from iuicss.template import render_to_response

def show_home(request):
    services = Service.all().filter('enabled = ', True).count()

    template_values = {
        'services': services,
    }
    
    return render_to_response(request, 'dnsalloc/show_home.html', template_values)

@login_required
def show_dashboard(request):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    create_form = ServiceForm()

    template_values = {
        'services': services,
        'create_form': create_form,
        'edit_form': None,
        'service': None,
        'message': None,
    }

    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def create_item(request):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    create_form = ServiceForm(data=request.POST)

    if create_form.is_valid():
        service = create_form.save(commit=False)
        service.user = request.user.user
        service.userid = service.user.user_id()
        service.waiting = True
        service.put()
        create_form = None

    template_values = {
        'services': services,
        'create_form': create_form,
        'edit_form': None,
        'service': None,
        'message': None,
    }
    
    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def show_item(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))

    db.delete(Result.all(keys_only=True).filter('tstamp < ', datetime.datetime.now()-datetime.timedelta(days=7)).fetch(100))

    template_values = {
        'services': services,
        'create_form': None,
        'edit_form': None,
        'service': service,
        'message': None,
    }
    
    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def edit_item(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))
    edit_form = ServiceForm(instance=service, data=request.POST if request.method == 'POST' else None)
    edit_form.key = service.key()
    
    if edit_form.is_valid():
        service = edit_form.save(commit=False)
        service.user = request.user.user
        service.waiting = True
        service.put()
        edit_form = None
    
    template_values = {
        'services': services,
        'create_form': None,
        'edit_form': edit_form,
        'service': service,
        'message': None,
    }
    
    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def switch_item(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))
    service.enabled = not(service.enabled)
    service.put()
    create_form = ServiceForm()
    message = 'Switched service %s!' % ('on' if service.enabled else 'off')

    template_values = {
        'services': services,
        'create_form': create_form,
        'edit_form': None,
        'service': None,
        'message': message,
    }

    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def force_item(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))
    service.waiting = True
    service.put()
    message = 'The service will be updated on next IP check!'

    template_values = {
        'services': services,
        'create_form': None,
        'edit_form': None,
        'service': service,
        'message': message,
    }

    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def feed_item(request, id):
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))

    return HttpResponseRedirect(reverse('dnsalloc.views.feed_status', kwargs={'key': str(service.key())}))

@login_required
def delete_item(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))
    service.delete()
    create_form = ServiceForm()
    message = 'Deleted service from your Dashboard!'

    template_values = {
        'services': services,
        'create_form': create_form,
        'edit_form': None,
        'service': None,
        'message': message,
    }

    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

@login_required
def delete_item_ask(request, id):
    services = Service.all().filter('userid = ', request.user.user.user_id()).order('-tstamp')
    service = get_object_or_404(Service, 'userid = ', request.user.user.user_id(), id=int(id))
    create_form = ServiceForm()
    message = 'Do you want to delete %s? <a href="%s" title="Yes">Yes</a>' % (service, reverse('dnsalloc.views.delete_item', kwargs={'id': id}))

    template_values = {
        'services': services,
        'create_form': create_form,
        'edit_form': None,
        'service': None,
        'message': message,
    }

    return render_to_response(request, 'dnsalloc/show_dashboard.html', template_values)

def feed_status(request, key):
    feedgen = ResultFeed('status', request).get_feed(key)
    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    
    return response
