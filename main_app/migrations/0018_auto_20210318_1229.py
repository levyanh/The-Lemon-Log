# Generated by Django 3.1.7 on 2021-03-18 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20210318_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='approved_comment',
            new_name='active',
        ),
    ]
