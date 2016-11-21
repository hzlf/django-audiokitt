# app_name/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<task>[-\w]+)/$', views.run_task, name='run-task'),
]
