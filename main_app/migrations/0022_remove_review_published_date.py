# Generated by Django 3.1.7 on 2021-03-18 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_auto_20210318_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='published_date',
        ),
    ]
