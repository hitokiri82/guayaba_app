from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'main.views.login_view'),
    url(r'^logout/$', 'main.views.logout'),
    url(r'^today/$', 'main.views.today'),
    url(r'^clients/$', 'clients.views.clients'),
    url(r'^clients/(?P<client_type>[^/]+)/create/$', 'clients.views.create_client'),
    url(r'^clients/(?P<client_id>\d*)/address/create/$', 'clients.views.create_address'),
    url(r'^clients/(?P<client_id>\d*)/phone/add/$', 'clients.views.add_phone_numbers'),
    url(r'^clients/(?P<client_id>\d*)/$', 'clients.views.client'),
    # url(r'^schedule/add/$', 'main.views.add_event'),
    # url(r'^schedule/event/(?P<event_id>\d+)/$', 'main.views.change_event'),
    # url(r'^$', 'guayaba.views.home', name='home'),
    # url(r'^guayaba/', include('guayaba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
