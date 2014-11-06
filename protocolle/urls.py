# coding: utf-8
from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

# from filebrowser.sites import site

urlpatterns = patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^/grappelli/grp-doc/', include('grappelli.urls')),
    url(r'^', include(admin.site.urls)),
    url(r'^flexselect/', include('flexselect.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)
