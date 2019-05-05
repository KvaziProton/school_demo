import os
import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """Get only the digits of the phone number."""

    phone = re.sub(r'\D', '', value)
    length = len(phone)

    if len(value) < 10 or length == 0:
        raise ValidationError(u'Please enter a valid phone number')
    # elif length < 10 or length > 11:
    #     raise ValidationError(u'Must be a 10 digit phone number')
    # elif length == 11:
    #     if not phone.startswith('1'):
    #         raise ValidationError(u'Must be a phone number in Canada')