# Generated by Django 3.1.2 on 2021-11-20 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20211120_0341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freeaddress',
            name='address_point',
        ),
    ]