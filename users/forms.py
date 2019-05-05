from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User

from .models import CustomUser, ROLE_CHOICES, StudentProfile, StudentCareer, ROLE_CHOICES, ENROLLEMENT_STATUS_CHOICES

class SignUpForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        }))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, initial='1')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }))
    confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Retype password',
            'class': 'form-control'
        }))

    def clean_email(self):
        email = self.cleaned_data['email']
        allowed_length = 254  # According to RFCs 3696 and 5321
        if len(email) > allowed_length:
            raise forms.ValidationError('An email address can be a maximum of '
                                        '{} characters'.format(allowed_length))

        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('The email address is invalid')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('The email address already exists')

        if not email.endswith('@baruch.cuny.edu'):
            raise forms.ValidationError('Use your Baruch hosted email')

        return email

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if len(password) < 6:
    #         raise forms.ValidationError('Password should be longer then 6 symbols')

    def clean(self):
        password = self.cleaned_data.get('password', None)
        confirm = self.cleaned_data.get('confirm', None)
        if password and confirm:
            if password != confirm:
                raise forms.ValidationError('Passwords do not match!')

        return self.cleaned_data

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control'
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }))

from django.forms import modelformset_factory

class CareerForm(forms.ModelForm):
    class Meta:
        model = StudentCareer
        exclude = ['id', 'user']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    middle_name = forms.CharField()
    last_name = forms.CharField(required=False)
    email = forms.CharField()

    class Meta:
        model = StudentProfile
        exclude = ['user', 'career']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@baruch.cuny.edu'):
            raise forms.ValidationError('Use your Baruch hosted email')

        return email
