# Generated by Django 5.1.7 on 2025-03-08 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stadium', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stadiumbooking',
            name='status',
        ),
    ]
