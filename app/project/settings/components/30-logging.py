
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(lineno)-4s%(name)-32s %(levelname)-8s %(message)s",
            'datefmt' : "%H:%M:%S"
        },
        # 'colored': {
        #     '()': 'colorlog.ColoredFormatter',
        #     'format': '%(log_color)s%(lineno)-4s%(name)-32s %(levelname)-8s %(message)s',
        #     'log_colors': {
        #         'DEBUG': 'bold_black',
        #         'INFO': 'green',
        #         'WARNING': 'yellow',
        #         'ERROR': 'red',
        #         'CRITICAL': 'bold_red',
        #     },
        # },
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },

    },
    'handlers': {
        'console':{
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        "rq_console": {
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        },
    },
    'loggers': {
        'audiokitt': {
            'handlers':['console',],
            'propagate': False,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers':['console',],
            'propagate': True,
            'level':'WARNING',
        },
        "rq.worker": {
            "handlers": ["rq_console",],
            "level": "DEBUG"
        },
    }
}
