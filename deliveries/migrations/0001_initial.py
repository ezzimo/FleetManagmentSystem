# Generated by Django 3.1.2 on 2021-09-01 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name_reciever', models.CharField(max_length=50)),
                ('destination_address', models.CharField(max_length=250)),
                ('destination_post_code', models.CharField(max_length=20)),
                ('operation_date', models.DateField(verbose_name='desired pickup date')),
                ('boxes_number', models.PositiveIntegerField(default=1, verbose_name='Number of Boxes')),
                ('boxes_wight', models.PositiveIntegerField(default=1, verbose_name='Boxes Wight')),
                ('boxes_volume', models.PositiveIntegerField(default=0, verbose_name='Boxes Volume')),
                ('document', models.FileField(help_text='Delivery Documets', upload_to='documents/deliveries_documents/', verbose_name='Delivery Certificates')),
                ('invoice', models.BooleanField(default=False, verbose_name='check if you want an invoice')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('total_paid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('delivery_key', models.CharField(max_length=200)),
                ('billing_status', models.BooleanField(default=False)),
                ('delivery_status', models.BooleanField(default=False)),
                ('destination_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_city', to='account.city')),
                ('pickup_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickup_address', to='account.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_user', to='account.customer')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Subcontractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, unique=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=150, unique=True, verbose_name='Last Name')),
                ('is_company', models.BooleanField(default=False, verbose_name='Is Active')),
                ('company_name', models.CharField(max_length=150, unique=True, verbose_name='Company Name')),
                ('ice', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='ICE of the Company')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('mobile', models.CharField(blank=True, max_length=150, verbose_name='Mobile Number')),
                ('mobile_2', models.CharField(blank=True, max_length=150, verbose_name='Mobile Number')),
                ('landline', models.CharField(blank=True, max_length=150, verbose_name='Landline Number')),
                ('address_line_1', models.CharField(max_length=255, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(max_length=255, verbose_name='Address Line 2')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor_city', to='account.city')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcontractor_vehicle', to='vehicle.vehicle')),
            ],
            options={
                'verbose_name': 'Subcontractor',
                'verbose_name_plural': 'Subcontractor',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_date', models.DateTimeField(verbose_name='Round Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='vehicle.vehicle')),
            ],
            options={
                'verbose_name': 'Round',
                'verbose_name_plural': 'Rounds',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='deliveries.delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_items', to='account.customer')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subcontract', models.BooleanField(default=False)),
                ('subcontract_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_loader', models.BooleanField(default=False)),
                ('loader_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_commission', models.BooleanField(default=False)),
                ('commission_coast', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_driver_charges', models.BooleanField(default=False)),
                ('driver_charges_coast', models.DecimalField(decimal_places=2, max_digits=7)),
                ('distance', models.PositiveSmallIntegerField(default=1, verbose_name='Approximative distance max=32767 km')),
                ('extra_time', models.DurationField(verbose_name='Extra time taken')),
                ('extra_time_coast', models.DecimalField(decimal_places=2, max_digits=7)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='deliveries.delivery')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round', to='deliveries.round')),
                ('subcontractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcontractor', to='deliveries.subcontractor')),
            ],
            options={
                'verbose_name': 'Delivery Details',
                'verbose_name_plural': 'Deliveries Details',
                'ordering': ('-created_at',),
            },
        ),
    ]