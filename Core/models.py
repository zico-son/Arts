from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import ValidationError 

def o6u_email_validator(value):
    if '@o6u.edu.eg' in value:
        return value
    else:
        raise ValidationError('Please use your O6U email address')


class User(AbstractUser):
    email = models.EmailField(validators=[o6u_email_validator], unique=True)
    account_type = models.CharField(max_length=50, default='student')
    pass
