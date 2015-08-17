# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _


class SubscriptionPluginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'))
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    plugin_id = forms.CharField(widget=forms.HiddenInput)
    redirect_url = forms.CharField(widget=forms.HiddenInput)
