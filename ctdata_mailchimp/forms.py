# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class SubscriptionPluginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'))
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    plugin_id = forms.CharField(widget=forms.HiddenInput)
    redirect_url = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(SubscriptionPluginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'mailchimp-subscription-form'
        self.helper.add_input(Submit('submit', 'Submit')) 
        self.helper.form_action = "admin:ctdata-mailchimp-subscribe"

class UnsubscribePluginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'))
    plugin_id = forms.CharField(widget=forms.HiddenInput)
    redirect_url = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(UnsubscribePluginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'mailchimp-subscription-form'
        self.helper.add_input(Submit('submit', 'Submit')) 
        self.helper.form_action = "admin:ctdata-mailchimp-unsubscribe"
