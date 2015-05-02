import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from controller.models import Cadet, Parent, Session


def pxlogin(request):
    response_dict = {'status': 'FAILED'}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(request, user)
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)          
                response_dict['status'] = 'OK'
                return HttpResponse(json.dumps(response_dict))
        else:
            # the authentication system was unable to verify the username and password
            return HttpResponse(json.dumps(response_dict))
    
    return render(request, 'controller/pages/login.html')


@login_required
def logout_view(request):
    logout(request)

@login_required
def dashboard(request):
    return render(request, 'controller/pages/index.html')

@login_required
def cadets_list(request):
    return render(request, 'controller/pages/tables.html')

@login_required
def get_cadet_list_json(request):
    column = ['full_name', 'age_today', 'gender', 'zip_code', 'city', 'state', 'country']
    cadet_list = list(Cadet.objects.values_list(*column))
    return HttpResponse(json.dumps(cadet_list))
    

