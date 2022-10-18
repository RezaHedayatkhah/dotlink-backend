from email import message
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    # phone_regex = RegexValidator(regex=r'((\+98)|0)[.\- ]?[0-9][.\- ]?[0-9][.\- ]?[0-9]', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True, blank=True, null=True) # validators should be a list
    # card_number = models.CharField(max_length=16)
    # id_code = models.CharField(max_length=256, blank=True, null=True)
    pass