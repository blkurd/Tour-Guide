# Generated by Django 4.1.7 on 2023-03-15 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_experience_user_trip_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='user',
        ),
    ]
