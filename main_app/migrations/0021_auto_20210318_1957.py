# Generated by Django 3.1.7 on 2021-03-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_auto_20210318_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=240),
        ),
    ]
