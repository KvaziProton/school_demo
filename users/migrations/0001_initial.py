# Generated by Django 2.1 on 2019-05-05 19:27

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('0', 'Admin'), ('1', 'General user')], default=1, max_length=2)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCareer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('employment_start_date', models.DateField()),
                ('employment_end_date', models.DateField(blank=True, null=True)),
                ('enrollment_status', models.CharField(choices=[('0', 'Full-time'), ('1', 'Alumni')], max_length=2)),
                ('salary_range', models.CharField(choices=[('1', '50,000 to 60,000'), ('2', '60,000 to 70,000'), ('3', '70,000 to 80,000'), ('4', '80,000 to 90,000'), ('5', '90,000 to 100,000')], max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('0', 'Male'), ('1', 'Female')], max_length=2)),
                ('phone_number', models.CharField(max_length=20, validators=[users.utils.validate_phone_number])),
                ('degree_type', models.CharField(choices=[('0', 'MD'), ('1', 'MBA'), ('2', 'BBA')], max_length=2)),
                ('graduation_date', models.DateField()),
                ('major1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='major1', to='users.Major')),
                ('major2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='major2', to='users.Major')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser')),
            ],
        ),
    ]
