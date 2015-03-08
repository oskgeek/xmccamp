from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'controller.views.index'),
]
