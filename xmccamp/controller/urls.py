from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'controller.views.pxlogin'),
    url(r'^home/$', 'controller.views.dashboard'),
    url(r'^logout/$', 'controller.views.logout_view'),
    url(r'^get_cadet_list_json/$', 'controller.views.get_cadet_list_json'),
]
