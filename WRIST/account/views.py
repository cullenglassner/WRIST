from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Added for login view
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse

# Import a user registration form
from account.forms import *
from django.shortcuts import get_object_or_404, render_to_response, render

# Import for json
import json





# Determines if the user is on a mobile device
def is_mobile(request):
    browser = request.META['HTTP_USER_AGENT']
    mobile = False
    if "Mobile" in browser:
        mobile = True
    return mobile



"""
        AUTHENTICATION VIEWS
"""
# User Register View
@csrf_protect
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/contacts/')
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['is_mobile'] = is_mobile(request)
    #Pass the context to a template
    return render_to_response('account/register.html', context)

# User Login View
@csrf_exempt
def user_login(request):
    """
    Login view
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/contacts/')
    else:
        form = AuthenticationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['is_mobile'] = is_mobile(request)
    #Pass the context to a template
    return render_to_response('account/login.html', context)

# User Logout View
@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



"""
        PROFILE VIEWS
"""
# User Profile View
@csrf_protect
@login_required(redirect_field_name='account/login.html')
def user_profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user':user, 'is_mobile':is_mobile(request)})

# User Profile Edit View
@csrf_protect
@login_required(redirect_field_name='account/login.html')
def user_profile_edit(request):
    form = UserEditForm()
    if request.method == 'POST':
        
        form = UserEditForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            gender = form.cleaned_data['gender']

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone_number = phone_number
            request.user.gender = gender
            request.user.save()
            return HttpResponseRedirect('/account/profile/')
    else:
        form = UserEditForm(
            initial={
                'uid':request.user.uid,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'phone_number':request.user.phone_number,
                'bio':request.user.bio,
                'gender':request.user.gender,
            },
        )
    return render(request, 'account/edit.html', {'form':form,
                                                 'is_mobile':is_mobile(request)})





# Profiles as seen by contacts
@csrf_protect
@login_required(redirect_field_name='account/login.html')
def public_profile(request, user_uid):
    target_user = get_object_or_404(get_user_model(), uid=user_uid)
    return render_to_response('account/public_profile.html', {'user':request.user,
                                                              'p_user':target_user,
                                                              'is_mobile':is_mobile(request)})

# Add contact by UID
@csrf_protect
@login_required(redirect_field_name='account/login.html')
def add_contact(request, contact_uid):
    target_user = get_object_or_404(get_user_model(), uid=contact_uid)
    # request.user.contacts.add(target_user.id)
    request.user.create_relationship(target_user)
    # request.user.save()
    return HttpResponseRedirect('/contacts/')