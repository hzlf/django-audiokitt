# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from authtools.models import AbstractEmailUser
from rest_framework.authtoken.models import Token

log = logging.getLogger(__name__)

class User(AbstractEmailUser):
    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):

    if created:
        token, token_created = Token.objects.get_or_create(user=instance)
        log.info('created token: {0} for {1}'.format(token, instance.email))