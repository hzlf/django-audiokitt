from rest_framework import serializers
from .models import Inquiry


class AnalyseRequestSerializer(serializers.ModelSerializer):
#class AnalyseRequestSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Inquiry
        fields = ('url', 'user', 'uuid', 'created', 'updated', 'file', 'comments',)

