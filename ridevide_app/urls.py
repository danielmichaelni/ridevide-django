from django.conf.urls import patterns, url
from ridevide_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^browse/(?P<ride_id>\d+)/$', views.browse_detail, name='browse_detail'),
    url(r'^browse/from_campus/$', views.browse_from_campus, name='browse_from_campus'),
    url(r'^browse/to_campus/$', views.browse_to_campus, name='browse_to_campus'),
    url(r'^delete_rider/(?P<ride_id>\d+)/$', views.delete_user_from_ride, name='delete_user_from_ride'),
    url(r'^add_rider/(?P<ride_id>\d+)/$', views.add_user_to_ride, name='add_user_to_ride'),
    url(r'^add/$', views.add, name='add'),
    url(r'^add/from_campus/$', views.add_from_campus, name='add_from_campus'),
    url(r'^add/to_campus/$', views.add_to_campus, name='add_to_campus'),
    url(r'^search/$', views.search, name='search'),
    url(r'^contact/$', views.contact, name='contact'),
)