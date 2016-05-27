# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from audiokitt.models import Analyse
from audiokitt.process import pipeline_task
from django.core.management.base import BaseCommand


class Worker(object):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.verbosity = int(kwargs.get('verbosity', 1))

        print
        print '/////////////////////////////////////////////////////////////'
        print '//                   AudioKITT CLI                         //'
        print '/////////////////////////////////////////////////////////////'
        print
        print 'id:      %s' % self.id
        print

    def run(self):
        if not self.id:
            print 'id is required!'
            sys.exit(2)

        a = Analyse.objects.get(id=self.id)

        pipeline_task(a)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'id',
            # nargs=1,
            type=int
        )

    def handle(self, *args, **options):
        runner = Worker(*args, **options)
        runner.run()
