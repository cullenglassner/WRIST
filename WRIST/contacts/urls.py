from django.conf.urls import patterns, include, url
from contacts.views import *


urlpatterns = patterns('',

    # Contact list.
    url(r'^$', contacts_list,name='contact_list'),
    url(r'^json_list/$', contacts_list_json,name='contact_list_json'),

    # Pending requests.
    url(r'^pending/$', pending_contacts_list,name='pending_contacts_list'),
    url(r'^json_pending_list/$', pending_contacts_list_json,name='pending_contact_list_json'),

    # Add a contact by UID.
    url(r'^add/(?P<contact_uid>\w+)/$', add_contact,name='add_contact'),
    url(r'^add_contact/$', add_contact_web,name='add_contact_web'),
    
    url(r'^json_add/', add_contact_json,name='add_contact_json'),

    # Delete a contact by UID.
    url(r'^remove_contact/$', remove_contact_web,name='remove_contact_web'),
)
