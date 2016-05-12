# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins, generics, viewsets

from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Inquiry, Analyse
from .serializers import AnalyseRequestSerializer
from .parsers import MultiPartFileUploadParser
from .util import md5_for_file




class AnalyseRequestViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    A simple ViewSet for listing or retrieving users.

        $ curl -v  -H "Authorization: Token 8148fdf6a0d0967f9355efdc17abla -F file=@file.mp3 http://localhost:8008/api/request/

    """

    #lookup_field = 'uuid'
    #lookup_value_regex = '[0-9a-f]{32}'

    queryset = Inquiry.objects.all()
    serializer_class = AnalyseRequestSerializer
    #authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    #permission_classes = (IsAuthenticated,)

    parser_classes = (MultiPartFileUploadParser,)

    def create(self, request, *args, **kwargs):

        #r = super(AnalyseRequestViewSet, self).create(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)


        print(serializer.data)

        print('-------------------------------')
        print(headers)
        print('-------------------------------')

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

        if serializer.instance.status == Analyse.STATUS_PENDING:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)

        if serializer.instance.status == Analyse.STATUS_DONE:
            return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):

        file = self.request.data.get('file')


        print('perform_create')

        print(md5_for_file(file))

        serializer.save(user=self.request.user, file=self.request.data.get('file'))

