from django import forms
from django.utils.safestring import mark_safe

def as_iui(self):
    "Returns this form rendered as HTML <div>s."
    return mark_safe(self._html_output(u'<div class="row">%(label)s%(field)s</div>', u'%s', '</div>', u'%s', False))

forms.ModelForm.as_iui = as_iui
