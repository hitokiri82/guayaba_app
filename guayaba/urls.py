from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'main.views.login_view'),
    url(r'^logout/$', 'main.views.logout'),
    url(r'^today/$', 'schedule.views.today'),
    url(r'^reports/$', 'main.views.reports_list'),
    url(r'^reports/profitability$', 'main.views.reports_test'),
    url(r'^clients/', include('clients.urls')),
    url(r'^appointments/', include('appointments.urls')),
    url(r'^schedule/$', 'main.views.this_month'),
    # url(r'^schedule/add/$', 'main.views.add_event'),
    # url(r'^schedule/event/(?P<event_id>\d+)/$', 'main.views.change_event'),
    # url(r'^$', 'guayaba.views.home', name='home'),
    # url(r'^guayaba/', include('guayaba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
