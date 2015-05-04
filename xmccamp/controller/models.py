from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError


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
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def parse_fields(self, data):
        try:
            self.name = data.get('Session name', '')
            self.location = data.get('Session location', '')
            self.session_type = data.get('Session type', '')
            self.end_date = data.get('Session end date', '')
            self.start_date = data.get('Session start date', '')

        except KeyError:
            pass


class Parent(models.Model):
    i_parent = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    cell_phone_number = models.CharField(max_length=255, blank=True, null=True)
    business_phone_number = models.CharField(max_length=255, blank=True, null=True)
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
                home_phone_number = data.get('Secondary P/G: Home phone number', '')
                cell_phone_number = data.get('Secondary P/G: Cell phone number', '')
                business_phone_number = data.get('Secondary P/G: Business phone number', '')
                user_profile.group = 'PS'
            else:
                full_name = data.get('Primary P/G: Name', '')
                gender = data.get('Primary P/G: Gender', '')
                email_address = data.get('Primary P/G: Email address', '')
                home_phone_number = data.get('Primary P/G: Home phone number', '')
                cell_phone_number = data.get('Primary P/G: Cell phone number', '')
                business_phone_number = data.get('Primary P/G: Business phone number', '')
                user_profile.group = 'PP'

            self.full_name = full_name
            self.gender = gender
            self.email_address = email_address
            self.home_phone_number = home_phone_number
            self.cell_phone_number = cell_phone_number
            self.business_phone_number = business_phone_number

            try:
                print "===============", full_name
                user = User.objects.create_user(username=full_name, password=email_address, email=email_address)
                user.save()
                user_profile.user = user
                user_profile.save()
                self.user = user_profile
                self.save()
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
    amount = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    remaining_amount = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    recieved_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.amount + self.currency


class Cadet(models.Model):
    sessions = models.ForeignKey(Session)
    i_cadet = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    age_today = models.IntegerField(max_length=255)
    dob = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    age_session = models.IntegerField(max_length=255, blank=True, null=True)
    primary_parent = models.ForeignKey(Parent, related_name='primary_parent')
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    contact_number = models.IntegerField(max_length=255, blank=True, null=True)
    secondary_parent = models.ForeignKey(Parent, related_name='secondary_parent')
    usac_training_program = models.CharField(max_length=255, blank=True, null=True)
    goal = models.TextField(blank=True, null=True, verbose_name="Why join XMC Camp?")

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
            self.contact_number = data.get('Participant: Home phone number', '')
            self.state = data.get('Participant: State', '')
            self.usac_training_program = data.get('Participant: USAC Training Program', '')
            self.zip_code = data.get('Participant: Zip code', '')
            self.goal = data.get('Participant: Please explain what you would like to have your son or daugher accomplish while at camp?  Explain any special situations or other information the staff should know about your child.', '')

        except KeyError as ex:
            print ex
            status = False

        except IntegrityError:
            status = False

        return status

class PXManager(models.Model):
    i_px_manager = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.full_name
