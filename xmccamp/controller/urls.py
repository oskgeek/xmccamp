from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'controller.views.login'),
    url(r'^home/$', 'controller.views.dashboard'),
]
