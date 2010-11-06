# -*- coding: utf-8 -*-
from django import forms
from dnsalloc.models import Service

class ServiceForm(forms.ModelForm):
    hostname = forms.RegexField(regex=r'^[\.\-a-zA-Z0-9]+$', required=True,
        label='Hostname', help_text='Type in the hostname you want to resolve. (e.g. myhost.dyndns.org)')
    username = forms.CharField(required=True,
        label='Username', help_text='Type in your DNS-O-Matic username.')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=True,
        label='Password', help_text='Type in your DNS-O-Matic password.')
    services = forms.RegexField(regex=r'^[\.\-a-zA-Z0-9]+$', required=False, initial='all.dnsomatic.com',
        label='Services', help_text='Type in the list of DNS-O-Matic services. (all.dnsomatic.com or hostnames: eg. FQDNs.)')

    class Meta:
        model = Service
        fields = ['hostname', 'username', 'password', 'services']
