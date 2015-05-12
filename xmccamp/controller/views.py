import uuid
import json

from django import forms
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from controller.models import UserProfile, Cadet, Parent, Session, Funds, CompleteTransaction, Product, SubTransaction, PXStaff
from controller.utils import mail, register_cadets, handle_uploaded_file, get_latest_payments


def pxlogin(request):
    response_dict = {'status': 'FAILED', 'Error': []}
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(username=email, password=password)

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
            # the authentication system was unable to verify the username and
            # password
            response_dict[
                'Error'] = 'Sorry, unable to verify provided credentials, try again!'
            return HttpResponse(json.dumps(response_dict))

    return render(request, 'controller/pages/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    context = {}
    context['permission'] = request.user.userprofile.group
    return render(request, 'controller/pages/index.html', context)


@login_required
def cadets_list(request):
    context = {}
    context['permission'] = request.user.userprofile.group
    return render(request, 'controller/pages/cadet_list.html', context)


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
        lookup = {'user__group': 'PP', 'secret_code__isnull': True}
        parent_qs = Parent.objects.filter(**lookup)
        for parent_obj in parent_qs:
            secret_code = str(uuid.uuid4())
            secret_code_url = "%s/Parent/Register/?code=%s" % (
                domain, secret_code)
            message_body = "To complete profile, follow this link: %s ." % secret_code_url
            print "Sending Email to : %s" % parent_obj.full_name
            mail(parent_obj.email_address,
                 "PX System Parent Registration! Complete your profile.",
                 message_body,
                 settings.MEDIA_ROOT + 'files_library/logo.png')
            parent_obj.secret_code = secret_code
            parent_obj.save()
            response_dict['status'] = 'OK'
        else:
            response_dict['status'] = 'FAILED'
            response_dict['Error'] = 'Sorry, please register a new parent to send registration email.'

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
            form_fields = {
                'i_parent': None, 'full_name': None, 'password': None,
                'gender': None, 'email_address': None, 'cell_phone_number': None,
                'business_phone_number': None, 'home_phone_number': None}

            for key in form_fields.iterkeys():
                form_fields[key] = request.POST.get(key, None)

            try:
                parent_obj = Parent.objects.get(
                    i_parent=form_fields['i_parent'])
                parent_obj.full_name = form_fields['full_name']
                parent_obj.user.user.set_password(form_fields['password'])
                parent_obj.user.user.username = form_fields['email_address']
                parent_obj.user.user.email = form_fields['email_address']
                parent_obj.user.user.save()
                parent_obj.gender = form_fields['gender']
                parent_obj.email_address = form_fields['email_address']
                parent_obj.cell_phone_number = form_fields['cell_phone_number']
                parent_obj.business_phone_number = form_fields[
                    'business_phone_number']
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
                register_cadets(
                    settings.MEDIA_ROOT + 'files_library/xmcamp.xlsx', msg)
                if msg['status'] != 'FAILED':
                    msg['status'] = 'OK'

    except Exception as ex:
        msg['status'] = 'FAILED'
        msg['Error'] = repr(ex)

    return HttpResponse(json.dumps(msg))


@login_required
def parent_list(request):
    context = {}
    context['permission'] = request.user.userprofile.group
    return render(request, 'controller/pages/parent_list.html', context)


@login_required
def get_parent_list_json(request):
    column = ['full_name', 'gender', 'email_address', 
    'cell_phone_number', 'business_phone_number', 'home_phone_number', 
    'funds__remaining_amount', 'funds__is_active']
    parent_list = list(Parent.objects.filter(user__group='PP').values_list(*column))
    parent_list = [row for row in parent_list if row[7] == True or row[7] is None]
    return HttpResponse(json.dumps(parent_list))


@login_required
def get_parent_fund_amount(request):
    fund_str = dict(amount="0.00 USD")
    lookup = {'parent__user__user': request.user, 'is_active': True}
    try:
        fund_obj = Funds.objects.get(**lookup)
        fund_str['amount'] = "%s %s" % (
            str(fund_obj.remaining_amount), fund_obj.currency)
    except Funds.DoesNotExist:
        pass
    return HttpResponse(json.dumps(fund_str))


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


@login_required
def get_cadet_purchase_history(request):
    response = dict(status='UNKNOWN', Error=[])
    try:
        if request.method == 'GET':
            column = ['cadet__full_name', 'transaction__product__name', 'transaction__quantity',
                      'transaction__cost', 'created_time']
            lookup = {'cadet__primary_parent__user__user': request.user}
            recent_transc_data = list(CompleteTransaction.objects.filter(
                **lookup).order_by('created_time').values_list(*column))

            for idx, row in enumerate(recent_transc_data):
                recent_transc_data[idx] = row[:4] + (str(row[4].date()),)
            response['status'] = 'OK'
            response['data'] = recent_transc_data

    except Exception as ex:
        response['status'] = 'FAILED'
        response['Error'] = repr(ex)

    return HttpResponse(json.dumps(response))


class ProductList(ListView):
    model = Product
    fields = '__all__'
    template_name = 'controller/pages/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        object_list = list(context['object_list'].values_list())
        object_list = [x + ('',) for x in object_list]
        context['object_list'] = json.dumps(object_list)
        context['permission'] = self.request.user.userprofile.group
        return context
        
    @classmethod
    def as_view(cls):
        return login_required(super(ProductList, cls).as_view())        


class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'controller/pages/product_create_form.html'
    success_url = '/Canteen/product/'
    
    @classmethod
    def as_view(cls):
        return login_required(super(ProductCreate, cls).as_view())    


class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'controller/pages/product_update_form.html'
    success_url = '/Canteen/product/'
    
    @classmethod
    def as_view(cls):
        return login_required(super(ProductUpdate, cls).as_view())    


class ProductDelete(DeleteView):
    model = Product
    fields = '__all__'
    success_url = '/Canteen/product/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
        
    @classmethod
    def as_view(cls):
        return login_required(super(ProductDelete, cls).as_view())


@login_required
@transaction.non_atomic_requests
def manage_transactions(request):
    response = dict(status='UNKNOWN', Error=[])
    try:
        if request.method == 'POST':
            cadet_id = request.POST.get('cadet_id', None)
            total_cost = float(request.POST.get('total_cost', 0))
            items = []
            for key in request.POST.keys():
                if 'product-' in key:
                    row_id = key.split('-')[-1]
                    product_id = request.POST[key]
                    cost = request.POST['product_cost-%s' % row_id]
                    quantity = request.POST['quantity-%s' % row_id]
                    items.append((product_id, quantity, cost))

            try:
                parent = Cadet.objects.get(pk=cadet_id).primary_parent
                lookup = {'parent': parent, 'is_active': True}
                fund_obj = Funds.objects.get(**lookup)
                if fund_obj.remaining_amount < total_cost:
                    raise ValueError

            except (Funds.DoesNotExist, Cadet.DoesNotExist):
                raise ValueError

            tObj = CompleteTransaction()
            tObj.cadet_id = cadet_id
            tObj.total_cost = total_cost
            tObj.save()

            for (product_id, quantity, cost) in items:
                sObj = SubTransaction()
                sObj.product_id = product_id
                sObj.quantity = quantity
                sObj.cost = float(cost)
                sObj.save()
                tObj.transaction.add(sObj)

            fund_obj.remaining_amount -= total_cost
            fund_obj.save()

            response['status'] = 'OK'
        else:
            context = {}
            column = ['i_product', 'name', 'cost_per_unit']
            product_list = list(Product.objects.values_list(*column))
            column = ['pk', 'full_name']
            cadet_list = list(Cadet.objects.values_list(*column))
            context['product_list'] = product_list
            context['cadet_list'] = cadet_list
            context['permission'] = request.user.userprofile.group
            return render(request, 'controller/pages/cart.html', context=context)

    except ValueError as ex:
        print ex
        response['status'] = 'FAILED'
        response['Error'] = 'Sorry, unable to continue due to low credit.'

    except Exception as ex:
        print ex
        response['status'] = 'FAILED'
        response['Error'] = repr(ex)

    return HttpResponse(json.dumps(response))



class PXStaffList(ListView):
    model = PXStaff
    fields = '__all__'
    template_name = 'controller/pages/accounts/account_list.html'

    def get_context_data(self, **kwargs):
        context = super(PXStaffList, self).get_context_data(**kwargs)
        column = ['i_px_manager', 'full_name', 'account_type', 'email_address']
        object_list = list(context['object_list'].values_list(*column))
        object_list = [x + ('',) for x in object_list]
        context['object_list'] = json.dumps(object_list)
        context['permission'] = self.request.user.userprofile.group
        return context
        
    @classmethod
    def as_view(cls):
        return login_required(super(PXStaffList, cls).as_view())


class PXStaffCreate(CreateView):
    model = PXStaff
    fields = ['full_name', 'email_address', 'password', 'account_type']
    template_name = 'controller/pages/accounts/account_create_form.html'
    success_url = '/Admin/accounts/'
    
    def get_context_data(self, **kwargs):
        context = super(PXStaffCreate, self).get_context_data(**kwargs)
        context['permission'] = self.request.user.userprofile.group
        return context
    
    def get_form(self, form_class):
        form = super(PXStaffCreate, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form
        
    def form_valid(self, form):
        email = form.cleaned_data['email_address']
        password = form.cleaned_data['password']
        group = form.cleaned_data['account_type']
        user = User.objects.create_user(
                    username=email, password=password, email=email)
        user.save()
        user_profile = UserProfile()
        user_profile.group = group
        user_profile.user = user
        user_profile.save()
        form.instance.user = user_profile
        return super(PXStaffCreate, self).form_valid(form)
        
    @classmethod
    def as_view(cls):
        return login_required(super(PXStaffCreate, cls).as_view())


class PXStaffUpdate(UpdateView):
    model = PXStaff
    fields = ['full_name', 'email_address', 'password', 'account_type']
    template_name = 'controller/pages/accounts/account_update_form.html'
    success_url = '/Admin/accounts/'
    
    def get_context_data(self, **kwargs):
        context = super(PXStaffUpdate, self).get_context_data(**kwargs)
        context['permission'] = self.request.user.userprofile.group
        return context
        
    def get_form(self, form_class):
        form = super(PXStaffUpdate, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        form.fields['email_address'].widget.attrs['readonly'] = True
        return form
    
    @classmethod
    def as_view(cls):
        return login_required(super(PXStaffUpdate, cls).as_view())


class PXStaffDelete(DeleteView):
    model = PXStaff
    fields = '__all__'
    success_url = '/Admin/accounts/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
        
    def get_object(self, queryset=None):
        obj = super(PXStaffDelete, self).get_object()
        obj.user.user.delete()
        obj.user.delete()
        return obj
        
    @classmethod
    def as_view(cls):
        return login_required(super(PXStaffDelete, cls).as_view())
