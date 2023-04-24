from django.core.exceptions import ValidationError

def o6u_email_validator(value):
    if '@o6u.edu.eg' in value:
        return value
    else:
        raise ValidationError('Please use your O6U email address')
