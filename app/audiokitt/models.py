# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import uuid
import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, UUIDField

from .util import md5_for_file

log = logging.getLogger(__name__)


def get_upload_path(instance, filename):

    filename, extension = os.path.splitext(filename)
    folder = "audiokitt/inquiry/%s/" % '/'.join(str(instance.uuid).split('-'))
    return os.path.join(folder, "%s%s" % (filename.lower(), extension.lower()))



class StatusModelMixin(models.Model):

    STATUS_PENDING = 0
    STATUS_DONE = 1
    STATUS_LOCKED = 2
    STATUS_ERROR = 99
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_DONE, 'Done'),
        (STATUS_LOCKED, 'Locked'),
        (STATUS_ERROR, 'Error'),
    )

    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        abstract = True


class TimestampedModelMixin(models.Model):

    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    class Meta:
        abstract = True



class Analyse(StatusModelMixin, TimestampedModelMixin, models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(null=True, upload_to=get_upload_path)
    file_md5 = models.CharField(max_length=32, null=True, db_index=True, unique=True)

    class Meta:
        app_label = 'audiokitt'
        verbose_name = _('Analyse')
        verbose_name_plural = _('Analyses')
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.filename)

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.path)

    def save(self, skip_apply_import_tag=False, *args, **kwargs):

        if self.file and not self.file_md5:
            self.file_md5 = md5_for_file(self.file)

        super(Analyse, self).save(*args, **kwargs)


class Inquiry(TimestampedModelMixin, models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(null=True, upload_to=get_upload_path)
    comments = models.TextField(null=True, blank=True)
    analyse = models.ForeignKey(Analyse, null=True, related_name='inquiries', on_delete=models.SET_NULL)

    class Meta:
        app_label = 'audiokitt'
        verbose_name = _('Inquiry')
        verbose_name_plural = _('Inquiries')
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.filename)

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.path)

    @property
    def file_md5(self):
        if self.file:
            return md5_for_file(self.file)

    @property
    def status(self):
        if self.analyse:
            return self.analyse.status


@receiver(pre_save, sender=Inquiry, dispatch_uid="inquiry_pre_save")
def inquiry_pre_save(sender, instance, **kwargs):
    log.debug('pre save: {}'.format(instance.file.path))

    if instance.file:

        qs = Analyse.objects.filter(file_md5=instance.file_md5)
        if qs.exists():
            instance.analyse = qs[0]
        else:

            analyse = Analyse(file=instance.file)
            analyse.save()

            instance.analyse = analyse




