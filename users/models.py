from django.contrib.auth.models import User
from django.db import models

from .utils import validate_phone_number

ROLE_CHOICES = (
    ('0', 'Admin'),
    ('1', 'General user')
)

GENDER_CHOICES = (
    ('0', 'Male'),
    ('1', 'Female')
)

DEGREE_CHOICES = (
    ('0', 'MS'),
    ('1', 'MBA'),
    ('2', 'BBA')
)

class CustomUser(User):
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=1,
    )
    middle_name = models.CharField(max_length=100, blank=True, null=True)

class Major(models.Model):
    major_name = models.CharField(max_length=100)

    def __str__(self):
        return self.major_name

SALARY_RANGE_CHOICES = (
    ('1', '50,000 to 60,000'),
    ('2', '60,000 to 70,000'),
    ('3','70,000 to 80,000'),
    ('4', '80,000 to 90,000'),
    ('5', '90,000 to 100,000')
)

ENROLLEMENT_STATUS_CHOICES = (
    ('0', 'Full-time'),
    ('1', 'Intern')
)

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100)
    industry_type = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20,
                                    validators=[validate_phone_number])
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class StudentCareer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True )
    job_role = models.CharField(max_length=100, blank=True, null=True)
    employment_start_date = models.DateField(blank=True, null=True)
    employment_end_date = models.DateField(blank=True, null=True)
    enrollment_status = models.CharField(
        max_length=2,
        choices=ENROLLEMENT_STATUS_CHOICES,
        blank=True, null=True
    )
    salary_range = models.CharField(
        max_length=5,
        choices=SALARY_RANGE_CHOICES,
    blank = True, null = True
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             blank=True, null=True)

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20,
                                    validators=[validate_phone_number])

    major1 = models.ForeignKey(Major, related_name='major1',
                               on_delete=models.CASCADE)
    major2 = models.ForeignKey(Major, related_name='major2',
                               on_delete=models.CASCADE, blank=True, null=True)
    degree_type = models.CharField(
        max_length=2,
        choices=DEGREE_CHOICES
    )
    graduation_date = models.DateField()

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    major1 = models.ForeignKey(Major, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,
                                    validators=[validate_phone_number])
    # admin_title = models.CharField(max_length=200)

