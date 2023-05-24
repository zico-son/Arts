from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.validators import o6u_email_validator

class User(AbstractUser):
    student = 'student'
    instructor = 'instructor'
    admin = 'admin'
    account_type_choices = [
        (student, 'student'),
        (instructor, 'instructor'),
        (admin, 'admin'),
    ]
    email = models.EmailField(validators=[o6u_email_validator], unique=True)
    account_type = models.CharField(max_length=10, choices=account_type_choices, default=student)