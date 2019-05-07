# Generated by Django 2.1 on 2019-05-07 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_adminprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcareer',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Company'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='degree_type',
            field=models.CharField(choices=[('0', 'MS'), ('1', 'MBA'), ('2', 'BBA')], max_length=2),
        ),
    ]
