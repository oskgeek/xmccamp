from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', \
        {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'', include('controller.urls')), 
    url('^.*/$', 'controller.views.pxlogin'),
)
