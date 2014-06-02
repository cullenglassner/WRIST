# Controls
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError

# Security
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Authentication
from account.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Contacts forms
from contacts.forms import *






# Determines if the user is on a mobile device
def is_mobile(request):
    browser = request.META['HTTP_USER_AGENT']
    mobile = False
    if "Mobile" in browser:
        mobile = True
    return mobile





########################### CONTACTS VIEWS ###########################
@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def contacts_list(request):
    user = request.user
    uid = request.user.uid
    relationship_list = user.get_relationships(1)
    pending_relationship_list = user.get_relationships(3)
    contact_list = []
    pending_contact_list = []
    for relationship in relationship_list:
        contact_list.append(relationship)
        #contact_list.append(relationship.from_user)
    for p_relationship in pending_relationship_list:
        pending_contact_list.append(p_relationship.from_user)
    return render_to_response('contacts/contact_list.html', 
                              {'user':user,'uid':uid,
                               'contact_list':contact_list,
                               'pending_contact_list':pending_contact_list,
                               'is_mobile':is_mobile(request)})

@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def pending_contacts_list(request):
    user = request.user
    uid = request.user.uid
    pending_relationship_list = user.get_relationships(3)
    pending_contact_list = []
    for relationship in pending_relationship_list:
        pending_contact_list.append(relationship.from_user)
    return render_to_response('contacts/pending_contact_list.html', 
                              {'user':user,'uid':uid,
                               'pending_contact_list':pending_contact_list,
                               'is_mobile':is_mobile(request)})



@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_contact(request):
    form = AddContactForm()
    if request.method == "POST":
        form = AddContactForm(request, data=request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            address = form.cleaned_data['address']
            target_user = get_object_or_404(get_user_model(), uid=uid)
            request.user.create_relationship(target_user, address)
            request.user.save()
            #return render_to_response('countacts/contact_list.html', {'user':request.user,
            #                                                          'is_mobile':is_mobile(request)})
            return HttpResponseRedirect('/contacts/')
    else:
        form = AddContactForm()
    return render_to_response('contacts/add.html', {'user':request.user,'uid':request.user.uid,
                                                    'form':form,
                                                    'is_mobile':is_mobile(request)})

@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def remove_contact(request):
    form = RemoveContactForm()
    if request.method == "POST":
        form = RemoveContactForm(request, data=request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            target_user = get_object_or_404(get_user_model(), uid=uid)
            request.user.remove_relationship(target_user, 1)
            #return render_to_response('countacts/contact_list.html', {'user':request.user,
            #                                                          'is_mobile':is_mobile(request)})
            return HttpResponseRedirect('/contacts/')
    else:
        form = RemoveContactForm()
    return render_to_response('contacts/remove.html', {'user':request.user, 'uid':request.user.uid,
                                                       'form': form,
                                                       'is_mobile':is_mobile(request)})




########################### OPEN API VIEWS ###########################
@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_contact_url(request, contact_uid, address):
    target_user = get_object_or_404(get_user_model(), uid=contact_uid)
    request.user.create_relationship(target_user, address)
    return HttpResponseRedirect('/contacts/')

@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_pending_contact_url(request, contact_uid):
    target_user = get_object_or_404(get_user_model(), uid=contact_uid)
    request.user.create_relationship(target_user, "")
    return HttpResponseRedirect('/contacts/')

@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def remove_contact_url(request, contact_uid):
    target_user = get_object_or_404(get_user_model(), uid=contact_uid)
    # request.user.contacts.add(target_user.id)
    request.user.create_relationship(target_user)
    # request.user.save()
    return HttpResponseRedirect('/contacts/')


