# Generated by Django 4.0.3 on 2022-03-28 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_userprofile_branch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='UID',
        ),
    ]
