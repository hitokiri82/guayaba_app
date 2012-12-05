from django.conf.urls import patterns, url

urlpatterns = patterns('clients.views',
    url(r'^$', 'clients'),
    url(r'^(?P<client_id>\d*)/$', 'client'),
    url(r'^(?P<client_type>[^/]+)/basic/create/$', 'client_basic'),
    url(r'^(?P<client_type>[^/]+)/basic/(?P<client_id>\d*)/$', 'client_basic'),
    url(r'^(?P<client_id>\d*)/address/$', 'create_address'),
    url(r'^(?P<client_id>\d*)/phones/$', 'phone_numbers'),
    url(r'^(?P<client_id>\d*)/phones/(?P<operation>[^/]+)/(?P<phone_id>\d*)/$', 'phone_numbers'),
)
