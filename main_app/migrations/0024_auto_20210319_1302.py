# Generated by Django 3.1.7 on 2021-03-19 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_auto_20210318_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_image',
            field=models.ImageField(blank=True, null=True, upload_to='review_pics'),
        ),
    ]