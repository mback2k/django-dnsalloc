from google.appengine.ext import webapp

def date(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg is None:
        arg = settings.DATE_FORMAT
    content = '''<abbr class="datetime d" title="%s">%s</abbr>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg)
    )
    return content

def time(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg is None:
        arg = settings.TIME_FORMAT
    content = '''<abbr class="datetime t" title="%s">%s</abbr>''' % (
        value.isoformat(),
        defaultfilters.time(value, arg)
    )
    return content

def datetime(value, arg1=None, arg2=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg1 is None:
        arg1 = settings.DATE_FORMAT
    if arg2 is None:
        arg2 = settings.TIME_FORMAT
    content = '''<abbr class="datetime dt" title="%s">%s %s</abbr>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg1),
        defaultfilters.time(value, arg2)
    )
    return content

def localedate(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg is None:
        arg = settings.DATE_FORMAT
    content = '''<abbr class="datetime ld" title="%s">%s</abbr>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg)
    )
    return content

def localetime(value, arg=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg is None:
        arg = settings.TIME_FORMAT
    content = '''<abbr class="datetime lt" title="%s">%s</abbr>''' % (
        value.isoformat(),
        defaultfilters.time(value, arg)
    )
    return content

def localedatetime(value, arg1=None, arg2=None):
    from django.conf import settings
    from django.template import defaultfilters
    if not value:
        return ''
    if arg1 is None:
        arg1 = settings.DATE_FORMAT
    if arg2 is None:
        arg2 = settings.TIME_FORMAT
    content = '''<abbr class="datetime ldt" title="%s">%s %s</abbr>''' % (
        value.isoformat(),
        defaultfilters.date(value, arg1),
        defaultfilters.time(value, arg2)
    )
    return content

register = webapp.template.create_template_register()
register.filter(date)
register.filter(time)
register.filter(datetime)
register.filter(localedate)
register.filter(localetime)
register.filter(localedatetime)
