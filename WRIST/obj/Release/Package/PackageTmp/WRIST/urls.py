from WRIST.views import *
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', main_page),

	# JSON Login view
    # url(r'^json_login/$', json_login_page),

    # Contacts APP URLs
	url(r'^contacts/', include('contacts.urls')),

    # Account App URLs
    url(r'^account/', include('account.urls')),

    # Admin site
    url(r'^admin/', include(admin.site.urls)),

	# Serve static content
	# url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
)
