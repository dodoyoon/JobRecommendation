from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^interest/$', views.interest, name='interest'),
    path('job_list', views.job_list, name='job_list'),
]
