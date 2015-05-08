from django.conf.urls import url
from controller.views import ProductList, ProductCreate, ProductUpdate, ProductDelete, \
    PXStaffList, PXStaffCreate, PXStaffUpdate, PXStaffDelete


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
    url(r'^Parent/get_parent_fund_amount/$',
        'controller.views.get_parent_fund_amount'),
    url(r'^Parent/fetch_funds/$', 'controller.views.fetch_funds'),
    url(r'^Parent/get_cadet_purchase_history/$',
        'controller.views.get_cadet_purchase_history'),
    url(r'Canteen/product/$', ProductList.as_view(), name='product_list'),
    url(r'Canteen/product/create/$',
        ProductCreate.as_view(), name='product_add'),
    url(r'Canteen/product/(?P<pk>[0-9]+)/$',
        ProductUpdate.as_view(), name='product_update'),
    url(r'Canteen/product/(?P<pk>[0-9]+)/delete/$',
        ProductDelete.as_view(), name='product_delete'),
    url(r'Canteen/manage_transactions/$',
        'controller.views.manage_transactions'),
    url(r'Admin/accounts/$', PXStaffList.as_view(), name='accounts_list'),
    url(r'Admin/accounts/create/$',
        PXStaffCreate.as_view(), name='accounts_add'),
    url(r'Admin/accounts/(?P<pk>[0-9]+)/$',
        PXStaffUpdate.as_view(), name='accounts_update'),
    url(r'Admin/accounts/(?P<pk>[0-9]+)/delete/$',
        PXStaffDelete.as_view(), name='accounts_delete'),
]
