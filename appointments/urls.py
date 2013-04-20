from django.conf.urls import patterns, url

urlpatterns = patterns('appointments.views',
    url(r'^$', 'add'),
    url(r'professionals/area/(?P<area>\w*)/$', 'get_professionals'),
    url(r'slots/(?P<professional>\w*)/$', 'get_time_slots'),
    url(r'slots/area/(?P<area>\w*)/$', 'get_time_slots_area'),
)
