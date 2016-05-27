import magic
import os

from ..util.grapher import create_waveform_image, create_spectrogram_image, calculate_peaks


# from ..util.conversion import any_to_wav

def waveform(path, audio):
    # t = any_to_wav(path, path + '.wav')
    t = path + '.wav'
    w = create_waveform_image(t, path + '.png')

    data = {
        'waveform': {
            'file': path + '.png'
        },
    }

    return data


def spectrogram(path, audio):
    # t = any_to_wav(path, path + '.wav')
    t = path + '.wav'
    w = create_spectrogram_image(t, path + '.s.png')

    data = {
        'spectrogram': {
            'file': path + '.png'
        },
    }

    return data


def peaks(path, audio):
    # t = any_to_wav(path, path + '.wav')
    t = path + '.wav'
    peak_data = calculate_peaks(t)

    data = {
        'peaks': peak_data,
    }

    return data
