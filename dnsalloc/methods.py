from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from dnsalloc.models import Result
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers

def api_results(request, format='json'):
    if not format in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    results = Result.objects.order_by('-crdate')
    return HttpResponse(serializers.serialize(format, results, fields=('successful', 'crdate')), mimetype='application/%s' % format)
