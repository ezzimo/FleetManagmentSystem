# Generated by Django 3.1.2 on 2021-10-30 23:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210908_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='address',
            name='town_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.city', verbose_name='Town/City/State'),
        ),
    ]