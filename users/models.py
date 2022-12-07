from datetime import date
from email.policy import default
from django.db import models


from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    birthdate = models.DateField()
    bio = models.CharField(max_length=256)
    is_critic = models.BooleanField(default=False)
    updated_at = models.DateField(default=date.today())

    
    REQUIRED_FIELDS = ['email','first_name','last_name','birthdate']
