# -*- coding: utf-8 -*-

# TODO: split_settings complains on unicode-path
# from __future__ import unicode_literals

import os
from split_settings.tools import optional, include
site_settings = os.path.join(os.getcwd(), 'project/local_settings.py')

try:
    settings_path = os.environ['SETTINGS_PATH']
    if settings_path and os.path.isfile(settings_path):
        site_settings = settings_path
except KeyError as e:
    pass

include(
    'components/10-base.py',
    'components/11-apps.py',
    'components/12-db.py',
    'components/13-api.py',
    'components/30-logging.py',
    optional(site_settings),

    # via server based settings in etc (placed by ansible deployment tasks)
    optional('/etc/audiokitt/application-settings.py'),

    scope=locals()
)
