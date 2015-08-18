# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .views import SubscriptionView, UnsubscribeView
from .models import SubscriptionPlugin
from .forms import SubscriptionPluginForm, UnsubscribePluginForm


class SubscriptionCMSPlugin(CMSPluginBase):
    cache = False
    render_template = 'ctdata_mailchimp/snippets/_subscription.html'
    name = _('Subscription')
    model = SubscriptionPlugin
    module = _('MailChimpSubscribe')

    def render(self, context, instance, placeholder):
        request = context['request']
        context['form'] = SubscriptionPluginForm(initial={'plugin_id': instance.pk,
                                                          'redirect_url': request.get_full_path()})
        return context

    def get_subscription_view(self):
        return SubscriptionView.as_view()

    def get_plugin_urls(self):
        subscription_view = self.get_subscription_view()

        return patterns('',
            url(r'^subscribe/$', never_cache(subscription_view), name='ctdata-mailchimp-subscribe'),
        )

plugin_pool.register_plugin(SubscriptionCMSPlugin)

class UnsubscribeCMSPlugin(CMSPluginBase):
    cache = False
    render_template = 'ctdata_mailchimp/snippets/_unsubscribe.html'
    name = _('Unsubscribe')
    model = SubscriptionPlugin
    module = _('MailChimpSubscribe')

    def render(self, context, instance, placeholder):
        request = context['request']
        context['form'] = UnsubscribePluginForm(initial={'plugin_id': instance.pk,
                                                          'redirect_url': request.get_full_path()})
        return context

    def get_unsubscribe_view(self):
        return UnsubscribeView.as_view()

    def get_plugin_urls(self):
        unsubscribe_view = self.get_unsubscribe_view()

        return patterns('',
            url(r'^unsubscribe/$', never_cache(unsubscribe_view), name='ctdata-mailchimp-unsubscribe'),
        )

plugin_pool.register_plugin(UnsubscribeCMSPlugin)
