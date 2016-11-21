# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status, views
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Inquiry, Analyse
from .parsers import MultiPartFileUploadParser
from .serializers import InquirySerializer, AnalyseListSerializer, AnalyseDetailSerializer
from .util.file import md5_for_file


class InquiryViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A simple ViewSet for listing or retrieving users.

        $ curl -v  -H "Authorization: Token 01700f368af11535c604145c302a122986d1497d" -F comments="my comment" -F file=@file.mp3 http://localhost:8008/api/v1/inquiry/

    """

    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f\-]{36}'

    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    parser_classes = (MultiPartFileUploadParser,)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if serializer.instance.status == Analyse.STATUS_PENDING:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

        if serializer.instance.status == Analyse.STATUS_DONE:
            return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if instance.status == Analyse.STATUS_DONE:
            s = AnalyseListSerializer(instance.analyse, context={'request': request})
            headers = {'Location': s.data.get('url')}
            return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

        return Response(serializer.data)

    def perform_create(self, serializer):

        file = self.request.data.get('file')
        print(md5_for_file(file))

        serializer.save(user=self.request.user, file=self.request.data.get('file'))


class AnalyseViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f\-]{36}'
    queryset = Analyse.objects.all()
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AnalyseDetailSerializer
        return AnalyseListSerializer


class LatestObjectView(RetrieveAPIView):
    queryset = Analyse.objects.all()
    serializer_class = AnalyseDetailSerializer

    def get_object(self, *args, **kwargs):
        return self.queryset.first()
