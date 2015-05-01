from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'controller.views.pxlogin'),
    url(r'^home/$', 'controller.views.dashboard'),
    url(r'^cadets_list/$', 'controller.views.cadets_list'),
    url(r'^logout/$', 'controller.views.logout_view'),
    url(r'^get_cadet_list_json/$', 'controller.views.get_cadet_list_json'),
]
