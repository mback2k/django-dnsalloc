#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# The MIT License
# 
# Copyright (c) 2009 Marc Hörsken <info@marc-hoersken.de>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = 'Marc Hörsken'

from django import template

def unidate(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg is None:
        arg = settings.DATE_FORMAT
    content = '''<time datetime="%s" class="date">%s</time>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg)
    )
    return mark_safe(content)

def unitime(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg is None:
        arg = settings.TIME_FORMAT
    content = '''<time datetime="%s" class="time">%s</time>''' % (
        value.isoformat(),
        defaultfilters.time(value, arg)
    )
    return mark_safe(content)

def unidatetime(value, arg1=None, arg2=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg1 is None:
        arg1 = settings.DATE_FORMAT
    if arg2 is None:
        arg2 = settings.TIME_FORMAT
    content = '''<time datetime="%s" class="datetime">%s %s</time>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg1),
        defaultfilters.time(value, arg2)
    )
    return mark_safe(content)

def localedate(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg is None:
        arg = settings.DATE_FORMAT
    content = '''<time datetime="%s" class="localedate">%s</time>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg)
    )
    return mark_safe(content)

def localetime(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg is None:
        arg = settings.TIME_FORMAT
    content = '''<time datetime="%s" class="localetime">%s</time>''' % (
        value.isoformat(),
        defaultfilters.time(value, arg)
    )
    return mark_safe(content)

def localedatetime(value, arg1=None, arg2=None):
    from django.conf import settings
    from django.template import defaultfilters
    from django.utils.safestring import mark_safe
    if not value:
        return ''
    if arg1 is None:
        arg1 = settings.DATE_FORMAT
    if arg2 is None:
        arg2 = settings.TIME_FORMAT
    content = '''<time datetime="%s" class="localedatetime">%s %s</time>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg1),
        defaultfilters.time(value, arg2)
    )
    return mark_safe(content)

unidate.is_safe = True
unitime.is_safe = True
unidatetime.is_safe = True
localedate.is_safe = True
localetime.is_safe = True
localedatetime.is_safe = True

register = template.Library()
register.filter(unidate)
register.filter(unitime)
register.filter(unidatetime)
register.filter(localedate)
register.filter(localetime)
register.filter(localedatetime)
