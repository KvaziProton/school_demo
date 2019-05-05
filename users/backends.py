from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from .models import CustomUser


class EmailModelBackend(object):
    def authenticate(self, email=None, password=None):
        print('in auth')
        try:
            validate_email(email)
        except ValidationError:
            pass
        try:
            user = CustomUser.objects.get(email=email)
            print(user)
        except CustomUser.DoesNotExist:
            pass
        print(user)
        print(user.check_password(password))
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None