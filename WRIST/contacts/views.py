from django.shortcuts import get_object_or_404, render_to_response, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.contrib.auth import get_user_model
from account.models import *
from contacts.forms import *


# Used in JSON views
import json
from django.core import serializers


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
        contact_list.append(relationship.from_user)
    for p_relationship in pending_relationship_list:
        pending_contact_list.append(p_relationship.from_user)
    return render_to_response('contacts/contact_list.html', 
                              {'user':user,'uid':uid,
                               'contact_list':contact_list,
                               'pending_contact_list':pending_contact_list})

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
                               'pending_contact_list':pending_contact_list,})



@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_contact_web(request):
    if request.method == "POST":
        form = AddContactForm(request, data=request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            target_user = get_object_or_404(get_user_model(), uid=uid)
            #request.user.contacts.add(target_user.id)
            request.user.create_relationship(target_user)
            request.user.save()
            return HttpResponseRedirect('/contacts/')
    else:
        form = AddContactForm()
    return render(request, 'contacts/add.html', {
        'form': form,
    })

@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def remove_contact_web(request):
    if request.method == "POST":
        form = RemoveContactForm(request, data=request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']
            target_user = get_object_or_404(get_user_model(), uid=uid)
            #request.user.contacts.add(target_user.id)
            request.user.remove_relationship(target_user, 1)
            return HttpResponseRedirect('/contacts/')
    else:
        form = RemoveContactForm()
    return render(request, 'contacts/remove.html', {
        'form': form,
    })



########################### JSON VIEWS ###########################
@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_contact_json(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        try:
            uid = json_data['uid']
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        # testing
        target_user = get_object_or_404(get_user_model(), uid=uid)
        request.user.create_relationship(target_user)
        request.user.save()
        #end testing
        #try:
        #    target_user = get_user_model().objects.get(uid=uid)
        #except get_user_model().DoesNotExist:
        #    target_user=None
        #    return HttpResponseServerError("Server Error: There is no user with the UID " + uid)
        #request.user.create_relationship(target_user)
        # request.user.save()
        return HttpResponseRedirect('/contacts/')
    else:
        form = AddContactForm()
    return render(request, 'contacts/add.html', {
        'form': form,
    })


@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def contacts_list_json(request):
    user = request.user
    uid = request.user.uid
    relationship_list = user.get_relationships(1)
    contact_list = []
    for relationship in relationship_list:
        contact_list.append(relationship.from_user)

    serialized_queryset = serializers.serialize("json", contact_list)
    return HttpResponse(json.dumps(serialized_queryset), content_type="application/json")


@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def pending_contacts_list_json(request):
    user = request.user
    uid = request.user.uid
    relationship_list = user.get_relationships(3)
    contact_list = []
    for relationship in relationship_list:
        contact_list.append(relationship.from_user)

    serialized_queryset = serializers.serialize("json", contact_list)
    return HttpResponse(json.dumps(serialized_queryset), content_type="application/json")



########################### OPEN API VIEWS ###########################
@csrf_exempt
@login_required(redirect_field_name='account/login.html')
def add_contact(request, contact_uid):
    target_user = get_object_or_404(get_user_model(), uid=contact_uid)
    # request.user.contacts.add(target_user.id)
    request.user.create_relationship(target_user)
    # request.user.save()
    return HttpResponseRedirect('/contacts/')


