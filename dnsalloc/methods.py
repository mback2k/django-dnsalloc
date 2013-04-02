from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from dnsalloc.models import Result
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import condition
from django.core import serializers

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
    Result.objects.filter(crdate__lt=timezone.now()-datetime.timedelta(days=7)).delete()
    results = Result.objects.order_by('-crdate')
    output = serializers.serialize(format, results, fields=('successful', 'crdate'))
    return HttpResponse(output, mimetype='application/%s' % format)
