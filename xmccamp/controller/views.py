import uuid
import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from controller.models import Cadet, Parent, Session, Funds
from controller.utils import mail, register_cadets, handle_uploaded_file, get_latest_payments


def pxlogin(request):
    response_dict = {'status': 'FAILED', 'Error': []}
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
                response_dict['user_id'] = user.pk
                return HttpResponse(json.dumps(response_dict))
        else:
            # the authentication system was unable to verify the username and password
            response_dict['Error'] = 'Sorry, unable to verify provided credentials, try again!'
            return HttpResponse(json.dumps(response_dict))

    return render(request, 'controller/pages/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    context = dict()
    context['permission'] = request.user.userprofile.group
    return render(request, 'controller/pages/index.html', context)


@login_required
def cadets_list(request):
    return render(request, 'controller/pages/cadet_list.html')


@login_required
def get_cadet_list_json(request):
    column = ['full_name', 'primary_parent__full_name', 'age_today', 'gender',
              'zip_code', 'city', 'state', 'country']
    cadet_list = list(Cadet.objects.values_list(*column))
    return HttpResponse(json.dumps(cadet_list))


@login_required
def parent_send_emails(request):
    response_dict = {'status': 'UNKNOWN', 'Error': []}
    try:
        domain = request.build_absolute_uri('/')[:-1]
        parent_qs = Parent.objects.filter(user__group='PP')
        for parent_obj in parent_qs:
            secret_code = str(uuid.uuid4())
            secret_code_url = "%s/Parent/Register/?code=%s" % (domain, secret_code)
            message_body = "To complete profile, follow this link: %s ." % secret_code_url
            print "Sending Email to : %s" % parent_obj.full_name
            mail(parent_obj.email_address,
                "PX System Parent Registration! Complete your profile.",
                message_body,
                settings.MEDIA_ROOT + 'files_library/logo.png')
            parent_obj.secret_code = secret_code
            parent_obj.save()
        response_dict['status'] = 'OK'

    except Exception as ex:
        response_dict['status'] = 'FAILED'
        response_dict['Error'] = repr(ex)

    return HttpResponse(json.dumps(response_dict))


def parent_registration(request):
    form_fields = {}

    if 'code' in request.GET:
        secret_code = str(request.GET['code'])
        try:
            parent_obj = Parent.objects.get(secret_code=secret_code)
            form_fields = parent_obj.__dict__
        except Parent.DoesNotExist:
            pass

        if request.method == 'POST':
            form_fields = {'i_parent': None, 'full_name': None, 'password': None,
                'gender': None, 'email_address': None, 'cell_phone_number': None,
                'business_phone_number': None, 'home_phone_number': None }

            for key in form_fields.iterkeys():
                form_fields[key] = request.POST.get(key, None)

            try:
                parent_obj = Parent.objects.get(i_parent=form_fields['i_parent'])
                parent_obj.full_name = form_fields['full_name']
                parent_obj.user.user.set_password(form_fields['password'])
                parent_obj.gender = form_fields['gender']
                parent_obj.email_address = form_fields['email_address']
                parent_obj.cell_phone_number = form_fields['cell_phone_number']
                parent_obj.business_phone_number = form_fields['business_phone_number']
                parent_obj.home_phone_number = form_fields['home_phone_number']
                parent_obj.save()
                message = 'Successfully, saved your account changes.'
            except Parent.DoesNotExist:
                message = 'Sorry, Unable to save your account changes.'
            form_fields['message'] = message

    else:
        return render(request, 'controller/pages/unauthorized.html')

    return render(request, 'controller/pages/signup.html', context=form_fields)


@csrf_exempt
def cadet_registration(request):
    msg = dict(status='UNKNOWN', Error=[], count=0)
    try:
        if request.method == 'POST':
            handle_uploaded_file(request.FILES['workbook_path'], msg)
            if msg['status'] != 'FAILED':
                register_cadets(settings.MEDIA_ROOT + 'files_library/xmcamp.xlsx', msg)
                if msg['status'] != 'FAILED':
                    msg['status'] = 'OK'

    except Exception as ex:
        msg['status'] = 'FAILED'
        msg['Error'] = repr(ex)

    return HttpResponse(json.dumps(msg))


@login_required
def parent_list(request):
    return render(request, 'controller/pages/parent_list.html')


@login_required
def get_parent_list_json(request):
    column = ['full_name', 'gender', 'email_address', 'cell_phone_number',
              'business_phone_number', 'home_phone_number']
    parent_list = list(Parent.objects.filter(user__group='PP').values_list(*column))
    return HttpResponse(json.dumps(parent_list))


@login_required
def get_parent_fund_amount(request):
    fund_str = "0.00 USD"
    lookup = {'parent__user__user': request.user, 'is_active': True}
    try:
        fund_str = str(Funds.objects.get(**lookup))
    except Funds.DoesNotExist:
        pass
    return HttpResponse(fund_str)


@login_required
def fetch_funds(request):
    msg = dict(status='UNKNOWN', Error=[])
    try:
        if request.method == 'GET':
            get_latest_payments(msg)
            if msg['status'] != 'FAILED':
                msg['status'] = 'OK'

    except Exception as ex:
        msg['status'] = 'FAILED'
        msg['Error'] = repr(ex)

    return HttpResponse(json.dumps(msg))
