# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey



class SubscriptionPlugin(CMSPlugin):

    list_name = models.CharField(_('List Name'), max_length=40)
    assign_language = models.BooleanField(
        _('Save user\'s language'), default=True, help_text=_('Save the user\'s language based on the page language'))

    def __unicode__(self):
        return unicode(self.list_name)

