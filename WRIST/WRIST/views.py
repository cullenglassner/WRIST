from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model



# Index page, used for routing users
@csrf_exempt
def main_page(request):
    #if request.user.is_authenticated():
    #    user = request.user
    #    uid = user.uid
    #return render_to_response('index.html')
    if request.user.is_authenticated():
        user = request.user
        uid = request.user.uid
        return render_to_response('index.html', {'user':user,'uid':uid})
    return render_to_response('index.html')