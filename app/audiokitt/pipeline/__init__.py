# -*- coding: utf-8 -*-

import logging
#import essentia.standard
#from essentia.standard import *

from django.conf import settings

from ..util import module_member

log = logging.getLogger(__name__)

DEFAULT_PIPELINE = [
    'audiokitt.pipeline.base.fileinfo',
    'audiokitt.pipeline.visualise.spectrogram',
    'audiokitt.pipeline.essentia_extractors.rhythm',
    'audiokitt.pipeline.essentia_extractors.tonal',
    'audiokitt.pipeline.essentia_extractors.level',
    'audiokitt.pipeline.visualise.peaks',
]

PIPELINE = getattr(settings, 'AUDIOKITT_PIPELINE', DEFAULT_PIPELINE)



class Pipeline(object):

    def __init__(self, path, tasks=None):
        self.path = path
        self.audio = None
        self.tasks = tasks or PIPELINE

    def audio_from_path(self, path):

        mono_loader = essentia.standard.MonoLoader(filename=path, sampleRate=8000)
        mono_audio = mono_loader()
        essentia.standard.MonoWriter(filename=path + '.wav')(mono_audio)

        return mono_audio

    def run(self):

        if not self.audio:
            self.audio = self.audio_from_path(self.path)

        data = {}

        for task in self.tasks:
            task_fun = module_member(task)
            try:
                task_data = task_fun(self.path, self.audio)
                data.update(task_data)
            except Exception as e:
                log.warning('pipeline error: {0} - {1}'.format(task, e))

        return data
