from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'lancer_decompte/(?P<id>[0-9]+)$', views.lancer_decompte, name='lancer_decompte'),
    url(r'corriger_decompte/(?P<id>[0-9]+)/(?P<valeur>[0-9]+)$', views.corriger_decompte, name='corriger_decompte'),
    url(r'plus_interesse/(?P<id>[0-9]+)$', views.plus_interesse, name='plus_interesse'),
    url(r'interesse/(?P<id>[0-9]+)$', views.interesse, name='interesse'),
    url(r'statistiques$', views.statistiques, name='statistiques$'),
    url(r'appareils$', views.AppareilList.as_view(), name='appareils'),
    url(r'utilisations$', views.UtilisationList.as_view(), name='utilisations'),
]

urlpatterns = format_suffix_patterns(urlpatterns)