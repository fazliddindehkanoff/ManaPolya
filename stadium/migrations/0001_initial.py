# Generated by Django 5.1.7 on 2025-03-08 02:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StadiumImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='stadium_images/')),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='stadium.stadium')),
            ],
        ),
        migrations.CreateModel(
            name='StadiumBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('confirmed', 'Tasdiqlandi'), ('canceled', 'Bekor qilindi')], default='pending', max_length=10)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booked_times', to='stadium.stadium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('stadium', 'start_time', 'end_time'), name='unique_booking')],
            },
        ),
    ]
