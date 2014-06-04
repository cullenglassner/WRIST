from django.conf.urls import patterns, include, url
from account.views import *

urlpatterns = patterns('',


    # Account authentication
    # url(r'^register/$', user_register, name='register'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^login/$', user_login, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', user_logout, name='logout'),

    # Profile management
    url(r'^profile/$', user_profile, name='profile'),
    url(r'^edit/$', user_profile_edit, name='edit'),


    # Profile page viewable by public (MUST BE LAST)
    url(r'^profile/(?P<user_uid>\w+)/$', public_profile, name='public_profile'),
    
)
