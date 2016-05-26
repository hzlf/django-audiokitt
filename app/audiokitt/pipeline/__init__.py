import importlib
import sys
import essentia
from essentia.standard import *
import essentia.standard


DEFAULT_PIPELINE = [
    'audiokitt.pipeline.base.fileinfo',
    'audiokitt.pipeline.visualise.spectrogram',
    'audiokitt.pipeline.essentia_extractors.rhythm',
    'audiokitt.pipeline.essentia_extractors.tonal',
    'audiokitt.pipeline.essentia_extractors.level',
    'audiokitt.pipeline.visualise.peaks',
]

def import_module(name):
    __import__(name)
    return sys.modules[name]

def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)

class Pipeline(object):

    def __init__(self, path, tasks=None):
        self.path = path
        self.audio = None
        self.tasks = tasks or DEFAULT_PIPELINE


    def audio_from_path(self, path):

        mono_loader = essentia.standard.MonoLoader(filename=path, sampleRate=8000)
        mono_audio = mono_loader()

        stereo_loader = essentia.standard.AudioLoader(filename=path)
        stereo_audio = stereo_loader()

        essentia.standard.MonoWriter(filename=path + '.wav')(mono_audio)


        return mono_audio


    def run(self):

        if not self.audio:
            self.audio = self.audio_from_path(self.path)

        data = {}

        for task in self.tasks:
            task_fun = module_member(task)
            task_data = task_fun(self.path, self.audio)
            data.update(task_data)

        print(data)

        return data