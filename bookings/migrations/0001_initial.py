# Generated by Django 5.1.2 on 2024-10-22 16:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('about_work', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Transferred', 'Transferred')], default='Pending', max_length=20)),
                ('client_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider_bookings', to='users.provider')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=20)),
                ('payment_url', models.URLField(blank=True, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.bookingrequest')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='users.provider')),
            ],
        ),
        migrations.CreateModel(
            name='ProviderAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='users.provider')),
            ],
            options={
                'unique_together': {('provider', 'date', 'start_time')},
            },
        ),
    ]
