# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions, StrictButton


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
        self.helper.form_class = 'mailchimp-subscription-form form-horizontal' 
        self.helper.add_input(Submit('submit', 'Submit')) 
        self.helper.form_action = "admin:ctdata-mailchimp-subscribe" 
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                Fieldset(
                    'first_name',
                    'last_name',
                    'email'
                    )
                )

class UnsubscribePluginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'))
    plugin_id = forms.CharField(widget=forms.HiddenInput)
    redirect_url = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(UnsubscribePluginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'mailchimp-subscription-form form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Submit')) 
        self.helper.form_action = "admin:ctdata-mailchimp-unsubscribe"
        self.helper.layout = Layout(
                Fieldset(
                    'email'
                    )
                )
