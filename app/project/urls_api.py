

from django.conf.urls import url, include
from django.contrib import admin


from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

from audiokitt.views import AnalyseRequestViewSet

User = get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #lookup_field = 'email'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


router.register(r'user', UserViewSet)
router.register(r'inquiry', AnalyseRequestViewSet)


