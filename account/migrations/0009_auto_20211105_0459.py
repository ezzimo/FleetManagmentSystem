# Generated by Django 3.1.2 on 2021-11-05 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_address_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='town_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.region', verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(max_length=255, verbose_name='Adresse Ligne 1'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(max_length=255, verbose_name='Adresse Ligne 2'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_name',
            field=models.CharField(max_length=50, verbose_name="Nom d'Adresse"),
        ),
        migrations.AlterField(
            model_name='address',
            name='delivery_instructions',
            field=models.CharField(max_length=255, verbose_name='Instructions de Livraison'),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Phone N°'),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(max_length=50, verbose_name='Code-Postale'),
        ),
        migrations.AlterField(
            model_name='address',
            name='town_city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.city', verbose_name='Ville'),
        ),
    ]