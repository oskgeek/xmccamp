import datetime

from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    group = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.username


class Session(models.Model):
    i_session = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    session_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def parse_fields(self, data):
        try:
            self.name = data.get('Session name', '')
            self.location = data.get('Session location', '')
            self.session_type = data.get('Session type', '')

        except (KeyError, TypeError) as ex:
            print ex


class Parent(models.Model):
    GENDER_TYPE = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
    i_parent = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=6, blank=True, null=True, choices=GENDER_TYPE)
    email_address = models.EmailField(max_length=255, unique=True)
    cell_phone_number = models.CharField(max_length=255, blank=True, null=True)
    business_phone_number = models.CharField(
        max_length=255, blank=True, null=True)
    home_phone_number = models.CharField(max_length=255, blank=True, null=True)
    secret_code = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.full_name

    def create_parent_by_fields(self, data, level):
        status = True
        try:
            user_profile = UserProfile()
            if level == 'S':
                full_name = data.get('Secondary P/G: Name', '')
                gender = data.get('Secondary P/G: Gender', '')
                email_address = data.get('Secondary P/G: Email address', '')
                home_phone_number = data.get(
                    'Secondary P/G: Home phone number', '')
                cell_phone_number = data.get(
                    'Secondary P/G: Cell phone number', '')
                business_phone_number = data.get(
                    'Secondary P/G: Business phone number', '')
                user_profile.group = 'PS'
            else:
                full_name = data.get('Primary P/G: Name', '')
                gender = data.get('Primary P/G: Gender', '')
                email_address = data.get('Primary P/G: Email address', '')
                home_phone_number = data.get(
                    'Primary P/G: Home phone number', '')
                cell_phone_number = data.get(
                    'Primary P/G: Cell phone number', '')
                business_phone_number = data.get(
                    'Primary P/G: Business phone number', '')
                user_profile.group = 'PP'

            self.full_name = full_name
            self.gender = gender
            self.email_address = email_address
            self.home_phone_number = home_phone_number
            self.cell_phone_number = cell_phone_number
            self.business_phone_number = business_phone_number

            try:
                print "===============", full_name
                user = User.objects.create_user(
                    username=email_address, password=email_address, email=email_address)
                user.save()
                user_profile.user = user
                user_profile.save()
                self.user = user_profile
                self.save()

                funds_obj = Funds()
                funds_obj.parent = self
                funds_obj.amount = float(data.get('Initial_Funds', 0))
                funds_obj.remaining_amount = float(
                    data.get('Initial_Funds', 0))
                funds_obj.currency = 'USD'
                funds_obj.name = 'Initial'
                funds_obj.recieved_time = datetime.datetime.now()
                funds_obj.save()
            except (ValueError, IntegrityError) as ex:
                status = False

        except KeyError as ex:
            print ex
            status = False

        return status


class Funds(models.Model):
    i_funds = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    currency = models.CharField(max_length=255)
    remaining_amount = models.FloatField()
    is_active = models.BooleanField(default=True)
    recieved_time = models.DateTimeField()

    def __unicode__(self):
        return self.parent.full_name


class Cadet(models.Model):
    GENDER_TYPE = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
    sessions = models.ForeignKey(Session, blank=True, null=True, editable=False)
    i_cadet = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    age_today = models.IntegerField()
    gender = models.CharField(
        max_length=6, blank=True, null=True, choices=GENDER_TYPE)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField(max_length=255, blank=True, null=True)
    age_session = models.IntegerField(blank=True, null=True)
    primary_parent = models.ForeignKey(Parent, related_name='primary_parent', 
        verbose_name="Select Cadet's Parent")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    contact_number = models.IntegerField(blank=True, null=True)
    secondary_parent = models.ForeignKey(
        Parent, related_name='secondary_parent', blank=True, null=True, editable=False)
    usac_training_program = models.CharField(
        max_length=255, blank=True, null=True)
    goal = models.TextField(
        blank=True, null=True, verbose_name="Why join XMC Camp?")

    def __unicode__(self):
        return self.full_name

    def parse_fields(self, data):
        status = True
        try:
            self.full_name = data.get('Participant: Name', '')
            self.age_today = data.get('Participant: Age as of today', '')
            self.gender = data.get('Participant: Gender', '')
            self.address = data.get('Participant: Address', '')
            self.age_session = data.get('Participant: Age as of session', '')
            self.city = data.get('Participant: City', '')
            self.country = data.get('Participant: Country', '')
            self.dob = data.get('Participant: Date of birth', '')
            self.email_address = data.get('Participant: Email address', '')
            self.contact_number = data.get(
                'Participant: Home phone number', '')
            self.state = data.get('Participant: State', '')
            self.usac_training_program = data.get(
                'Participant: USAC Training Program', '')
            self.zip_code = data.get('Participant: Zip code', '')
            self.goal = data.get(
                'Participant: Please explain what you would like to have your son or daugher accomplish while at camp?  Explain any special situations or other information the staff should know about your child.', '')

        except KeyError as ex:
            print ex
            status = False

        except IntegrityError:
            status = False

        return status


class PXStaff(models.Model):
    ACCOUNT_TYPE = (('AD', 'Adminstrator'), ('CT', 'PX Staff'))
    i_px_manager = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE)

    def __unicode__(self):
        return self.full_name


class Product(models.Model):
    i_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    cost_per_unit = models.FloatField()

    def get_absolute_url(self):
        return reverse('product_list')

    def __unicode__(self):
        return self.name


class SubTransaction(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    cost = models.FloatField()

    def __unicode__(self):
        return 'Product Purchased %s with %d quantity' % (self.product.name, self.quantity)


class CompleteTransaction(models.Model):
    i_transaction = models.AutoField(primary_key=True)
    cadet = models.ForeignKey(Cadet)
    transaction = models.ManyToManyField(SubTransaction)
    total_cost = models.FloatField()
    created_time = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.cadet


class GeneralSettings(models.Model):
    i_settings = models.AutoField(primary_key=True)
    configuration = JSONField()

    def __unicode__(self):
        return "General Settings"


class RevertTransaction(models.Model):
    i_trans_revert = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(SubTransaction)
    created_by = models.ForeignKey(UserProfile, related_name='created_by')
    approved_by = models.ForeignKey(
        UserProfile, related_name='approved_by', blank=True, null=True)
    approved_time = models.DateTimeField(default=datetime.datetime.now)
    approval_status = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Replica of Transaction %s' % self.transaction


class StickyNotes(models.Model):
    i_note = models.AutoField(primary_key=True)
    i_parent = models.ForeignKey(Parent, blank=True, null=True, verbose_name='Please select Parent')
    i_cadet = models.ForeignKey(Cadet, blank=True, null=True, verbose_name='Please select Cadet')
    issued_by = models.ForeignKey(UserProfile, editable=False)
    issued_time = models.DateTimeField(default=datetime.datetime.now, editable=False)
    remarks = models.TextField()

    def __unicode__(self):
        return 'Note Issued to %s by %s' % (self.i_parent, self.issued_by)
