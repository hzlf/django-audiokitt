REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_MODEL_SERIALIZER_CLASS': [
        'rest_framework.serializers.HyperlinkedModelSerializer',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '60/minute'
    }

}