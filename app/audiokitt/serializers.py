from rest_framework import serializers

from .models import Inquiry, Analyse


class InquirySerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='status_display', read_only=True)

    class Meta:
        model = Inquiry
        # lookup_field = 'uuid'
        fields = (
            'url',
            # 'uuid',
            'created',
            'eta',
            'user',
            'status',
            'file'
        )

        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'user': {'lookup_field': 'uuid'}
        }


class AnalyseBaseSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='status_display', read_only=True)

    class Meta:
        model = Analyse
        fields = (
            'url',
            'status',
        )

        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }


class AnalyseListSerializer(AnalyseBaseSerializer):
    class Meta(AnalyseBaseSerializer.Meta):
        pass


class AnalyseDetailSerializer(AnalyseBaseSerializer):
    data = serializers.JSONField(source='analyse_data', read_only=True)

    class Meta(AnalyseBaseSerializer.Meta):
        fields = (
            'url',
            'status',
            'data',
        )
