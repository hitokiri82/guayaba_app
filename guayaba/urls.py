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
    url(r'^clients/$', 'main.views.clients'),

    # url(r'^schedule/add/$', 'main.views.add_event'),
    # url(r'^schedule/event/(?P<event_id>\d+)/$', 'main.views.change_event'),
    # url(r'^$', 'guayaba.views.home', name='home'),
    # url(r'^guayaba/', include('guayaba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
