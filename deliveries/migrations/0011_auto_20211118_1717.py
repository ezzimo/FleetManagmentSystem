# Generated by Django 3.1.2 on 2021-11-18 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0010_auto_20211111_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetails',
            name='commission_coast',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='delivery_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='driver_charges_coast',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='extra_time',
            field=models.DurationField(blank=True, null=True, verbose_name='Extra time taken'),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='extra_time_coast',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='is_commission',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='is_driver_charges',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='is_loader',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='is_subcontract',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='loader_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round', to='deliveries.round'),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='subcontract_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='deliverydetails',
            name='subcontractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcontractor', to='deliveries.subcontractor'),
        ),
    ]