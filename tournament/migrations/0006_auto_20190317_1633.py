# Generated by Django 2.1.7 on 2019-03-17 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_request'),
        ('tournament', '0005_invite'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Enrollment',
            new_name='Enrolment',
        ),
    ]