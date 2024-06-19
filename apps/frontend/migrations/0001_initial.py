# Generated by Django 5.0.6 on 2024-06-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('time', models.TimeField()),
                ('devname', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('devid', models.CharField(blank=True, max_length=100, null=True)),
                ('eventtime', models.BigIntegerField(db_index=True)),
                ('tz', models.CharField(blank=True, max_length=10, null=True)),
                ('logid', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('subtype', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('level', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('vd', models.CharField(blank=True, max_length=50, null=True)),
                ('srcip', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
                ('srcname', models.CharField(blank=True, max_length=255, null=True)),
                ('srcport', models.IntegerField(blank=True, null=True)),
                ('srcintf', models.CharField(blank=True, max_length=50, null=True)),
                ('srcintfrole', models.CharField(blank=True, max_length=50, null=True)),
                ('dstip', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
                ('dstport', models.IntegerField(blank=True, null=True)),
                ('dstintf', models.CharField(blank=True, max_length=50, null=True)),
                ('dstintfrole', models.CharField(blank=True, max_length=50, null=True)),
                ('srccountry', models.CharField(blank=True, max_length=100, null=True)),
                ('dstcountry', models.CharField(blank=True, max_length=100, null=True)),
                ('sessionid', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('proto', models.IntegerField(blank=True, null=True)),
                ('action', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('policyid', models.IntegerField(blank=True, db_index=True, null=True)),
                ('policytype', models.CharField(blank=True, max_length=50, null=True)),
                ('service', models.CharField(blank=True, max_length=100, null=True)),
                ('trandisp', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('sentbyte', models.BigIntegerField(blank=True, null=True)),
                ('rcvdbyte', models.BigIntegerField(blank=True, null=True)),
                ('sentpkt', models.BigIntegerField(blank=True, null=True)),
                ('rcvdpkt', models.BigIntegerField(blank=True, null=True)),
                ('appcat', models.CharField(blank=True, max_length=100, null=True)),
                ('crscore', models.CharField(blank=True, max_length=11, null=True)),
                ('craction', models.CharField(blank=True, max_length=11, null=True)),
                ('crlevel', models.CharField(blank=True, max_length=50, null=True)),
                ('srchwvendor', models.CharField(blank=True, max_length=100, null=True)),
                ('mastersrcmac', models.CharField(blank=True, max_length=50, null=True)),
                ('srcmac', models.CharField(blank=True, max_length=50, null=True)),
                ('srcserver', models.CharField(blank=True, max_length=11, null=True)),
            ],
            options={
                'db_table': 'logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=100)),
                ('system_type', models.CharField(choices=[('normal', 'Normal'), ('server', 'Server')], max_length=6)),
                ('system_ip', models.GenericIPAddressField()),
            ],
            options={
                'db_table': 'system_configuration',
            },
        ),
        migrations.CreateModel(
            name='SystemIPPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ip_range', models.GenericIPAddressField()),
                ('to_ip_range', models.GenericIPAddressField()),
            ],
            options={
                'db_table': 'system_ip_pool',
            },
        ),
    ]
