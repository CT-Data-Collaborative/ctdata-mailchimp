# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import FormView

from mailchimp.api import MailChimpAPI

from .utils import get_language_for_code
from .forms import SubscriptionPluginForm, UnsubscribePluginForm
from .models import SubscriptionPlugin


ERROR_MESSAGES = {
    104: _('Invalid API-Key'),
    200: _('The selected list does not exist.'),
    314: _('You are already subscribed to our list.'),
    330: _('You are already subscribed but you have not yet confirmed via the email.'),
    414: _('That email is not registered with us.'),
    430: _('That email has already been unsubscribed.'),
}

class SubscriptionView(FormView):

    form_class = SubscriptionPluginForm
    template_name = 'ctdata_mailchimp/subscription.html'

    def form_valid(self, form):
        h = MailChimpAPI(settings.MAILCHIMP_API_KEY)
        plugin = get_object_or_404(SubscriptionPlugin, pk=form.cleaned_data['plugin_id'])

        # merge_vars = None
        # if plugin.assign_language:
        #     language = get_language_for_code(self.request.LANGUAGE_CODE)
        #     if language:
        #         merge_vars = {'mc_language': language}

        try:
            h.subscribeList(list_name=plugin.list_name, user_email=form.cleaned_data['email'],\
             first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])

        except Exception as exc:
            try:
                message = ERROR_MESSAGES[exc.code]
            except (AttributeError, KeyError):
                message = ugettext(u'Oops, something must have gone wrong. Please try again later.')

            if self.request.user.is_superuser and hasattr(exc, 'code'):
                message = u'%s (MailChimp Error (%s): %s)'% (message, exc.code, exc)

            messages.error(self.request, message)
        else:
            messages.success(self.request, ugettext(u'You have successfully subscribed to our mailing list.'))
        return redirect(form.cleaned_data['redirect_url'])

    def form_invalid(self, form):
        redirect_url = form.data.get('redirect_url')

        if redirect_url:
            message = _(u'Please enter a valid email.')
            messages.error(self.request, message)
            response = HttpResponseRedirect(redirect_url)
        else:
            # user has tampered with the redirect_url field.
            response = HttpResponseBadRequest()
        return response

class UnsubscribeView(FormView):

    form_class = UnsubscribePluginForm
    template_name = 'ctdata_mailchimp/unsubscribe.html'

    def form_valid(self, form):
        h = MailChimpAPI(settings.MAILCHIMP_API_KEY)
        plugin = get_object_or_404(SubscriptionPlugin, pk=form.cleaned_data['plugin_id'])


        try:
            h.unsubscribeList(list_name=plugin.list_name, user_email=form.cleaned_data['email'])

        except Exception as exc:
            try:
                message = ERROR_MESSAGES[exc.code]
            except (AttributeError, KeyError):
                message = ugettext(u'Oops, something must have gone wrong. Please try again later.')

            if self.request.user.is_superuser and hasattr(exc, 'code'):
                message = u'%s (MailChimp Error (%s): %s)'% (message, exc.code, exc)

            messages.error(self.request, message)
        else:
            messages.success(self.request, ugettext(u'You have successfully unsubscribed from our mailing list.'))
        return redirect(form.cleaned_data['redirect_url'])

    def form_invalid(self, form):
        redirect_url = form.data.get('redirect_url')

        if redirect_url:
            message = _(u'Please enter a valid email.')
            messages.error(self.request, message)
            response = HttpResponseRedirect(redirect_url)
        else:
            # user has tampered with the redirect_url field.
            response = HttpResponseBadRequest()
        return response
