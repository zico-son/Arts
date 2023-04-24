from django.core.exceptions import ValidationError

def semester_year_validator(value):
    if value < 2000 or value > 2100:
        raise ValidationError('Year must be between four digits 20XX') 
