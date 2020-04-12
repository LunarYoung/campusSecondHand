from django.urls import re_path
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from add import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sellUpload/', views.up, name='up'),

    path('mything/', views.mything, name='thing'),

    path('thingStore/', views.paginator_view, name='All_thing'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('register/', views.register, name='register'),

    path('email/', views.re_email, name= 're_email'),

    path('edict/', views.edict, name='edict'),

    re_path(r'^thingStore/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sort/1', views.dianqi, name='sort1'),
    re_path(r'^sort/1/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sort/2', views.shuben, name='sort2'),
    re_path(r'^sort/2/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sort/3', views.jiaotong, name='sort3'),
    re_path(r'^sort/3/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sort/4', views.shenghuoyongpin, name='sort4'),
    re_path(r'^sort/4/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('sort/5', views.qita, name='sort5'),
    re_path(r'^sort/5/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('search/', views.search, name='search'),
    re_path(r'^search/(?P<pk>[0-9]+)/$', views.Thing_detail, name="detail"),

    path('need/', views.qiugou, name='qiugou'),

    path('upneed/', views.upneed, name='upneed'),
    path('myupneed/', views.myupneed, name='myupneed'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

