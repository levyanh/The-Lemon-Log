# Generated by Django 3.1.7 on 2021-03-16 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_userprofileinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofileinfo',
            old_name='picture',
            new_name='profile_pic',
        ),
    ]
