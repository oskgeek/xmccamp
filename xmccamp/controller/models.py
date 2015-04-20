from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    product = models.ForeignKey('products.Product',
                                limit_choices_to={'parent': None})
    
class Cadet(models.Model):      
    user = models.OneToOneField(User)

    full_name = models.CharField(max_length=255)  
    age_today = models.IntegerField(max_length=255)  
    age_session = models.IntegerField(max_length=255, blank=True, null=True)  
    contact_number = models.IntegerField(max_length=255, blank=True, null=True)  
    gender = models.CharField(max_length=5, blank=True, null=True)  
    email_address = models.CharField(max_length=255, blank=True, null=True)  
    city = models.CharField(max_length=255, blank=True, null=True)  
    country = models.CharField(max_length=255, blank=True, null=True)  
    
    dob = models.DateTimeField(blank=True, null=True)  
    state = models.CharField(max_length=255, blank=True, null=True)  
    zip_code = models.CharField(max_length=255, blank=True, null=True)  

    primary_parent = models.ForeignKey(Parent, related_name='primary_parent')
    secondary_parent = models.ForeignKey(Parent, related_name='secondary_parent')
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    
    usac_training_program = models.CharField(max_length=255, blank=True, null=True)  
    goal = models.TextField(blank=True, null=True, verbose_name="Why join XMC Camp?")
    

    def __unicode__(self):
        return u'Cadet Profile of user: %s' % self.user.username
