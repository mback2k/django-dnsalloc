# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import ServiceForm
from .feeds import ResultFeed
from .models import User, Service, Result
from .tasks import task_query_service

def migrate_social_auth(request):
    if request.user.is_authenticated():
        if not request.user.social_auth.filter(provider='google-oauth2').exists():
            button = '<a class="ym-button ym-next ym-success float-right" href="%s" title="Migrate Account">Migrate Account</a>' % reverse('social:begin', kwargs={'backend': 'google-oauth2'})
            messages.info(request, '%sPlease migrate your account from Google App Engine to Google OAuth 2.0 for Login (OpenID Connect)' % button)
            return True
    return False

def show_home(request):
    migrate_social_auth(request)

    users = User.objects.filter(is_active=True).count()
    services = Service.objects.filter(enabled=True).count()

    template_values = {
        'users': users,
        'services': services,
    }

    return render(request, 'show_home.html', template_values)


@login_required
def show_dashboard(request):
    migrate_social_auth(request)

    services = Service.objects.filter(user=request.user).order_by('hostname')
    create_form = ServiceForm()

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def show_service(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)

    template_values = {
        'services': services,
        'service': service,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def create_service(request):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    create_form = ServiceForm(data=request.POST)

    if create_form.is_valid():
        service = create_form.save(commit=False)
        service.user = request.user
        service.save()
        return HttpResponseRedirect(reverse('dnsalloc:show_service', kwargs={'service_id': service.id}))

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def edit_service(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    edit_form = ServiceForm(instance=service, data=request.POST if request.method == 'POST' else None)

    if edit_form.is_valid():
        service = edit_form.save(commit=False)
        service.user = request.user
        service.waiting = True
        service.save()
        return HttpResponseRedirect(reverse('dnsalloc:show_service', kwargs={'service_id': service.id}))

    template_values = {
        'services': services,
        'service': service,
        'service_edit_form': edit_form,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def switch_service(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.enabled = not(service.enabled)
    service.save()
    create_form = ServiceForm()

    messages.success(request, 'Switched service "%s" %s!' % (service, 'on' if service.enabled else 'off'))

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def force_service(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.waiting = True
    service.save()

    task_query_service.apply_async(args=[service.id])

    messages.success(request, 'The service "%s" will be updated on next IP check!' % service)

    template_values = {
        'services': services,
        'service': service,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def delete_service(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    service.delete()
    create_form = ServiceForm()

    messages.success(request, 'Deleted service "%s" from your Dashboard!' % service)

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render(request, 'show_dashboard.html', template_values)

@login_required
def delete_service_ask(request, service_id):
    services = Service.objects.filter(user=request.user).order_by('hostname')
    service = get_object_or_404(Service, user=request.user, id=service_id)
    create_form = ServiceForm()

    button = '<a class="ym-button ym-delete ym-danger float-right" href="%s" title="Yes">Yes</a>' % reverse('dnsalloc:delete_service', kwargs={'service_id': service_id})
    messages.warning(request, '%sDo you want to delete service "%s"?' % (button, service))

    template_values = {
        'services': services,
        'service_create_form': create_form,
    }

    return render(request, 'show_dashboard.html', template_values)


def show_status(request):
    template_values = {}
    return render(request, 'show_status.html', template_values)


def feed_service(request, service_id):
    feed = ResultFeed()
    return feed(request, service_id)

def redirect_login(request):
    from django.conf import settings
    return HttpResponseRedirect(settings.LOGIN_URL)
