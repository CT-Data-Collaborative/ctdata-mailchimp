# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class MailchimpUserMGMT(CMSApp):
    name = _('Mailchimp User Management')
    urls = ['ctdata_mailchimp.urls']


apphook_pool.register(MailchimpUserMGMT)
