from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^interest/$', views.interest, name='interest'),
    path('<pk>/update', views.BasicUpdate.as_view(), name='edit_basic'),
    path('<pk>/updateEdu', views.EduLevelUpdate.as_view(), name='edit_edu'),
    path('<pk>/updateCareer', views.CareerUpdate, name='edit_career'),
    path('<pk>/addEdu', views.EduLevelAdd.as_view(), name='add_edu'),
    path('<pk>/addCareer', views.CareerAdd.as_view(), name='add_career'),
    path('addLicense', views.LicenseAdd.as_view(), name='add_license'),
    path('addLicenseType', views.LicenseTypeAdd.as_view(), name='add_lictype'),
    path('<pk>/deleteLicense/', views.LicenseDelete.as_view(), name='delete_license'), 
    url(r'^for_me/$', views.personal, name='personal'),
    url(r'^job_list', views.job_list, name='job_list'),
    url(r'^job_detail/(?P<pk>[0-9]+)/$', views.job_detail, name='job_detail'),
    url(r'^search/$', views.search, name='search'),
]
