

from django.conf.urls import url, include
from django.contrib import admin


from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

from audiokitt.views import InquiryViewSet, AnalyseViewSet

User = get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'uuid', 'email')

        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f\-]{36}'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'inquiry', InquiryViewSet)
router.register(r'analyse', AnalyseViewSet)
