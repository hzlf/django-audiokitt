# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

def md5_for_file(file):
    """
    :param file
    :return str
    Calculate md5 hash for file-object
    """
    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)

    return md5.hexdigest()
