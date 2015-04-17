from django.db import models
from django.contrib.auth.models import User


class Cadet(models.Model):      
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=255)  
    session_name = models.CharField(max_length=255)  
    age = models.IntegerField(max_length=255)  
    email = models.CharField(max_length=255)  
    state = models.CharField(max_length=255)  
    zip_code = models.CharField(max_length=255)  
    session_end_date = models.DateTimeField()  
    session_start_date = models.DateTimeField()  
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
