from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^add$', 'core.views.add_entry', name='add'),
    url(r'^add/success$', 'core.views.add_success', name='add_success'),
    url(r'^sync$', 'core.views.sync', name='sync'),
    url(r'^kiosk$', 'core.views.kiosk', name='kiosk'),
    # url(r'^pasty/', include('pasty.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'core.views.login', name='login'),
)
