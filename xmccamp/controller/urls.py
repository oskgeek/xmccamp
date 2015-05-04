from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'controller.views.pxlogin'),
    url(r'^home/$', 'controller.views.dashboard'),
    url(r'^logout/$', 'controller.views.logout_view'),
    url(r'^cadets_list/$', 'controller.views.cadets_list'),
    url(r'^get_cadet_list_json/$', 'controller.views.get_cadet_list_json'),
    url(r'^parent_list/$', 'controller.views.parent_list'),
    url(r'^get_parent_list_json/$', 'controller.views.get_parent_list_json'),
    url(r'^Cadet/Register/$', 'controller.views.cadet_registration'),
    url(r'^Parent/SendEmails/$', 'controller.views.parent_send_emails'),
    url(r'^Parent/Register/$', 'controller.views.parent_registration'),
    url(r'^Parent/get_parent_fund_amount/$', 'controller.views.get_parent_fund_amount'),
    url(r'^Parent/fetch_funds/$', 'controller.views.fetch_funds'),
]
