# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import condition
from django.core import serializers
from django.utils import timezone
from .models import Result
import datetime

def api_results_etag(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return None
    return 'id-%d' % Result.objects.latest('crdate').id

def api_results_last_modified(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return None
    return Result.objects.latest('crdate').crdate

@condition(etag_func=api_results_etag, last_modified_func=api_results_last_modified)
def api_results(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    results = Result.objects.filter(crdate__gt=timezone.now()-datetime.timedelta(days=14)).order_by('-crdate')
    output = serializers.serialize(format, results, fields=('successful', 'crdate'))
    return HttpResponse(output, content_type='application/%s' % format)
