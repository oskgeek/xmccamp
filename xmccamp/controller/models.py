from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    i_session = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    session_type = models.CharField(max_length=255)
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def parse_fields(data):
        try:
            self.name = data['Session name']
            self.location = data['Session location']
            self.session_type = data['Session type']
            self.end_date = data['Session end date']
            self.start_date = data['Session start date']

        except KeyError:
            pass


class Parent(models.Model):
    i_parent = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    cell_phone_number = models.IntegerField(max_length=255, blank=True, null=True)
    business_phone_number = models.IntegerField(max_length=255, blank=True, null=True)
    home_phone_number = models.IntegerField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.full_name

    def parse_fields(data):
        try:
            self.full_name = data['Secondary P/G: Name']
            self.gender = data['Secondary P/G: Gender']
            self.email_address = data['Secondary P/G: Email address']
            self.home_phone_number = data['Secondary P/G: Home phone number']
            self.cell_phone_number = data['Secondary P/G: Cell phone number']
            self.business_phone_number = data['Secondary P/G: Business phone number']
        except KeyError:
            pass


class Cadet(models.Model):
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

    def parse_fields(data):
        try:
            self.full_name = data['Participant: Name']
            self.age_today = data['Participant: Age as of today']
            self.gender = data['Participant: Gender']
            self.address = data['Participant: Address']
            self.age_session = data['Participant: Age as of session']
            self.city = data['Participant: City']
            self.country = data['Participant: Country']
            self.dob = data['Participant: Date of birth']
            self.email_address = data['Participant: Email address']
            self.contact_number = data['Participant: Home phone number']
            self.state = data['Participant: State']
            self.usac_training_program = data['Participant: USAC Training Program']
            self.zip_code = data['Participant: Zip code']
            self.goal = data['Participant: Please explain what you would like to have your son or daugher accomplish while at camp?  Explain any special situations or other information the staff should know about your child.']

        except KeyError:
            pass

class PXManager(models.Model):
    i_px_manager = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.full_name
