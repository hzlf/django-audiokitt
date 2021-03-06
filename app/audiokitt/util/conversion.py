# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import subprocess

import audiotools
from django.conf import settings

log = logging.getLogger(__name__)

LAME_BINARY = getattr(settings, 'LAME_BINARY', 'lame')
SOX_BINARY = getattr(settings, 'SOX_BINARY', 'sox')
FAAD_BINARY = getattr(settings, 'FAAD_BINARY', 'faad')


def any_to_wav(src, dst):
    log.info('any to wav: %s > %s' % (src, dst))

    if not os.path.isfile(src):
        raise IOError('unable to access %s' % src)

    src_path, src_ext = os.path.splitext(src)
    if src_ext.lower() == '.wav':
        # shutil.copyfile(src, dst)
        return src

    try:
        audiotools.open(src).convert(dst, audiotools.WaveAudio)

    except Exception as e:

        log.info('file %s not supported by audiotools' % src)

        name, ext = os.path.splitext(src)

        if ext.lower() in ['.mp3', ]:
            mp3_to_wav(src, dst)

        if ext.lower() in ['.m4a', '.mp4']:
            m4a_to_wav(src, dst)

        print name
        print ext

    log.debug('to wav: %s > %s' % (src, dst))
    if os.path.exists(dst):
        return dst


def mp3_to_wav(src, dst):
    log.debug('mp3-to-wav converter: %s' % src)

    command = [
        SOX_BINARY,
        src,
        '-c 2',
        '-r 44100',
        dst
    ]

    log.debug('running: %s' % ' '.join(command))

    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout = p.communicate()

    if stdout:
        log.debug(stdout)


def m4a_to_wav(src, dst):
    log.debug('m4a-to-wav converter: %s' % src)

    command = [
        FAAD_BINARY,
        src,
        '-d', '-q',
        '-o', dst
    ]

    log.debug('running: %s' % ' '.join(command))

    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout = p.communicate()

    if stdout:
        log.debug(stdout)
