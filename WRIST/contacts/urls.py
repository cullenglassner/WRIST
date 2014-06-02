from django.conf.urls import patterns, include, url
from contacts.views import *


urlpatterns = patterns('',

########################### CONTACTS VIEWS ###########################
    # Contact list.
    url(r'^$', contacts_list, name='contact_list'),

    # Pending requests.
    url(r'^pending/$', pending_contacts_list, name='pending_contacts_list'),

    # Web form Add/Remove contacts.
    url(r'^add_contact/$', add_contact, name='add_contact'),
    url(r'^remove_contact/$', remove_contact, name='remove_contact'),



########################### OPEN API VIEWS ###########################
    # URL request Add/Remove contacts.
    url(r'^add/(?P<contact_uid>\w+)/(?P<address>\w+)/$', add_contact_url, name='add_contact_url'),
    url(r'^add_pending_contact/(?P<contact_uid>\w+)/$', add_pending_contact_url, name='add_pending_contact'),
    url(r'^remove/(?P<contact_uid>\w+)/$', remove_contact_url, name='remove_contact_url'),
)
