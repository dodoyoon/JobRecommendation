from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^interest/$', views.interest, name='interest'),
    url(r'^for_me/$', views.personal, name='personal'),
    url(r'^job_list', views.job_list, name='job_list'),
    url(r'^job_detail/(?P<pk>[0-9]+)/$', views.job_detail, name='job_detail'),
]
