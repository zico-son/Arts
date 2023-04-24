from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.validators import o6u_email_validator

class User(AbstractUser):
    email = models.EmailField(validators=[o6u_email_validator], unique=True)
    account_type = models.CharField(max_length=50, default='student')
