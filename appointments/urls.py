from django.conf.urls import patterns, url

urlpatterns = patterns('appointments.views',
    url(r'^first_step/$', 'external_add1'),
    url(r'^second_step/$', 'external_add2'),
    url(r'^appointment_success/$', 'external_add3'),
    url(r'^professionals/area/(?P<area>\w*)/$', 'get_professionals'),
    url(r'^slots/(?P<professional>\w*)/$', 'get_time_slots'),
    url(r'^slots/area/(?P<area>\w*)/$', 'get_time_slots_area'),
    # url(r'^mockup/$', 'mockup'),
)
