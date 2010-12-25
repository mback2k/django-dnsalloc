import datetime
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from dnsalloc.forms import ServiceForm
from dnsalloc.feeds import ResultFeed
from dnsalloc.models import Service, Result
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages

def show_home(request):
    services = Service.objects.all().filter(enabled=True).count()

    template_values = {
        'services': services,
    }
    
    return render_to_response('show_home.html', template_values, context_instance=RequestContext(request))


@login_required
def show_dashboard(request):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    create_form = ServiceForm()

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def create_service(request):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    create_form = ServiceForm(data=request.POST)

    if create_form.is_valid():
        service = create_form.save(commit=False)
        service.user = request.user
        service.save()
        create_form = None

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }
    
    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def show_service(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)

    Result.objects.all().filter(crdate__lt=datetime.datetime.now()-datetime.timedelta(days=7)).delete()

    template_values = {
        'services': services,
        'service': service,
    }
    
    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def edit_service(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    edit_form = ServiceForm(instance=service, data=request.POST if request.method == 'POST' else None)
    
    if edit_form.is_valid():
        service = edit_form.save(commit=False)
        service.user = request.user
        service.waiting = True
        service.save()
        edit_form = None
    
    template_values = {
        'services': services,
        'service': service,
        'service_edit_form': edit_form,
    }
    
    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def switch_service(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.enabled = not(service.enabled)
    service.save()
    create_form = ServiceForm()
    
    messages.success(request, 'Switched service %s!' % ('on' if service.enabled else 'off'))
    
    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def force_service(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.waiting = True
    service.save()
    
    messages.success(request, 'The service will be updated on next IP check!')
    
    template_values = {
        'services': services,
        'service': service,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def delete_service(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.delete()
    create_form = ServiceForm()
    
    messages.success(request, 'Deleted service from your Dashboard!')
    
    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))

@login_required
def delete_service_ask(request, service_id):
    services = Service.objects.all().filter(user=request.user).order_by('-tstamp')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    create_form = ServiceForm()
    
    messages.warning(request, 'Do you want to delete %s? <a href="%s" title="Yes">Yes</a>' % (service, reverse('dnsalloc.views.delete_service', kwargs={'service_id': service_id})))
    
    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render_to_response('show_dashboard.html', template_values, context_instance=RequestContext(request))


def feed_service(request, service_id):
    feed = ResultFeed()
    return feed(request, service_id)

def feed_service_key(request, service_key):
    from google.appengine.ext import db
    return HttpResponseRedirect(reverse('dnsalloc.views.feed_service', kwargs={'service_id': db.Key(service_key).id()}))
