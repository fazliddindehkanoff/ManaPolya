# Generated by Django 5.1.7 on 2025-03-08 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('owner', 'Stadion egasi'), ('user', 'Foydalanuvchi')], default='user', max_length=10),
        ),
    ]
