# Generated by Django 5.0.6 on 2024-06-21 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_alter_systemconfiguration_system_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='systemconfiguration',
            constraint=models.UniqueConstraint(fields=('system_name', 'system_ip'), name='unique_system_name_system_ip'),
        ),
    ]