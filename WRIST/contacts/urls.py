from django.conf.urls import patterns, include, url
from contacts.views import *


urlpatterns = patterns('',

    # Contact list.
    url(r'^$', contacts_list, name='contact_list'),

    # Pending requests.
    url(r'^pending/$', pending_contacts_list, name='pending_contacts_list'),

    # Add a contact by UID.
    url(r'^add/(?P<contact_uid>\w+)/(?P<address>\w+)/$', add_contact, name='add_contact'),
    url(r'^add_contact/$', add_contact_web, name='add_contact_web'),

    # Delete a contact by UID.
    url(r'^remove/(?P<contact_uid>\w+)/$', remove_contact, name='remove_contact'),
    url(r'^remove_contact/$', remove_contact_web, name='remove_contact_web'),
)
