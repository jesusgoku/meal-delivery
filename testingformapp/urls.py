from django.conf.urls import url

from testingformapp import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^menu/$', views.MenuListView.as_view(), name='menu_list'),
    url(r'^menu/create/$', views.MenuCreateView.as_view(), name='menu_create'),
    url(r'^menu/(?P<menu_id>[\d\w-]+)/update/$', views.MenuUpdateView.as_view(), name='menu_update'),
    url(r'^menu/(?P<menu_id>[\d\w-]+)/$', views.MenuDetailView.as_view(), name='menu_detail'),
    url(r'^menu/(?P<menu_id>[\d\w-]+)/order/$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'^menu/(?P<menu_id>[\d\w-]+)/order/create$', views.OrderCreateView.as_view(), name='order_create'),
]
