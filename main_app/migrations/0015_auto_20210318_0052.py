# Generated by Django 3.1.7 on 2021-03-18 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_auto_20210318_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]
