# Generated by Django 3.1.2 on 2021-11-03 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deliveries', '0003_auto_20211101_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_user', to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='user_pickup',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_pickup', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]