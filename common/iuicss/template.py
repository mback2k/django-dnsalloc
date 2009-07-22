# -*- coding: utf-8 -*-
import os, re

def is_iphone(request):
    if 'HTTP_USER_AGENT' in request.META:
        return re.search(r'Mobile.*Safari', request.META['HTTP_USER_AGENT']) is not None
    else:
        return False

def render_to_response(request, template, *args, **kwargs):
    try:
        from ragendja.template import render_to_response as render
    except:
        from django.shortcuts import render_to_response as render
    if is_iphone(request):
        return render(request, '%s/iphone/%s' % (os.path.dirname(template), os.path.basename(template)), *args, **kwargs)
    else:
        return render(request, template, *args, **kwargs)
