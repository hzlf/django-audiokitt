
import magic
import os

from essentia.standard import *
from essentia import Pool

def rhythm(path, audio):

    bpm_fn = RhythmExtractor()
    bpm = bpm_fn(audio)[0]

    danceability_fn = Danceability()
    danceability = danceability_fn(audio)

    energy_fn = Energy()
    energy = energy_fn(audio)

    loudness_fn = Loudness()
    loudness = loudness_fn(audio)

    data = {
        'rhythm': {
            'bpm': bpm,
            'danceability': danceability,
            'energy': energy,
            'loudness': loudness,
        },
    }

    return data

def tonal(path, audio):

    fn = TonalExtractor()
    res = fn(audio)

    data = {
        'tonal': {
            'key': res[9],
            'scale': res[10],
        },
    }

    return data

def level(path, audio):
    res = ReplayGain()(audio)


    data = {
        'level': {
            'replaygain': res
        },
    }

    return data