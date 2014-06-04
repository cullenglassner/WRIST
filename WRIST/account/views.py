# Control
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render

# Security
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Forms
from account.forms import *
from django.views.generic.edit import FormView







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
class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm
    success_url = 'account/login.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/account/login')

class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    success_url = 'contacts/contact_list.html'

    def form_valid(self, form):
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect('/contacts/')
        return HttpResponseRedirect('/account/login')

#@csrf_exempt
#def user_register(request):
#    if request.method == 'POST':
#        form = UserRegistrationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            #return HttpResponseRedirect('/contacts/')
#            return HttpResponseRedirect('/')
#    else:
#        form = UserRegistrationForm()
#    context = {}
#    context.update(csrf(request))
#    context['form'] = form
#    context['is_mobile'] = is_mobile(request)
#    #Pass the context to a template
#    return render_to_response('account/register.html', context)

#@csrf_exempt
#def user_login(request):
#    """
#    Login view
#    """
#    if request.method == 'POST':
#        form = AuthenticationForm(data=request.POST)
#        if form.is_valid():
#            user = authenticate(username=request.POST['username'],
#                                password=request.POST['password'])
#            if user is not None:
#                login(request, user)
#                return HttpResponseRedirect('/contacts/')
#    else:
#        form = AuthenticationForm()
#    context = {}
#    context.update(csrf(request))
#    context['form'] = form
#    context['is_mobile'] = is_mobile(request)
#    #Pass the context to a template
#    return render_to_response('account/login.html', context)

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
            residence_city = form.cleaned_data['residence_city']
            residence_state = form.cleaned_data['residence_state']
            job_title = form.cleaned_data['job_title']
            job_employer = form.cleaned_data['job_employer']

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone_number = phone_number
            request.user.gender = gender
            request.user.residence_city = residence_city
            request.user.residence_state = residence_state
            request.user.job_title = job_title
            request.user.job_employer = job_employer
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
                'residence_city':request.user.residence_city,
                'residence_state':request.user.residence_state,
                'job_title':request.user.job_title,
                'job_employer':request.user.job_employer,
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
