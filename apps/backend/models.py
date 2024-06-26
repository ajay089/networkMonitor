from django.db import models

class Logs(models.Model):
    date = models.DateField(db_index=True)
    time = models.TimeField()
    devname = models.CharField(max_length=255, blank=True, null=True)
    devid = models.CharField(max_length=100, blank=True, null=True)
    eventtime = models.BigIntegerField()
    tz = models.CharField(max_length=10, blank=True, null=True)
    logid = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    subtype = models.CharField(max_length=50, blank=True, null=True, db_index=True)  # Index for subtype
    level = models.CharField(max_length=50, blank=True, null=True)
    vd = models.CharField(max_length=50, blank=True, null=True)
    srcip = models.GenericIPAddressField(blank=True, null=True)
    srcname = models.CharField(max_length=255, blank=True, null=True)
    srcport = models.IntegerField(blank=True, null=True)
    srcintf = models.CharField(max_length=50, blank=True, null=True)
    srcintfrole = models.CharField(max_length=50, blank=True, null=True)
    dstip = models.GenericIPAddressField(blank=True, null=True)
    dstport = models.IntegerField(blank=True, null=True)
    dstintf = models.CharField(max_length=50, blank=True, null=True)
    dstintfrole = models.CharField(max_length=50, blank=True, null=True)
    srccountry = models.CharField(max_length=100, blank=True, null=True)
    dstcountry = models.CharField(max_length=100, blank=True, null=True)
    sessionid = models.BigIntegerField(blank=True, null=True)
    proto = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True, db_index=True)  # Index for action
    policyid = models.IntegerField(blank=True, null=True)
    policytype = models.CharField(max_length=50, blank=True, null=True)
    service = models.CharField(max_length=100, blank=True, null=True)
    trandisp = models.CharField(max_length=50, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    sentbyte = models.BigIntegerField(blank=True, null=True)
    rcvdbyte = models.BigIntegerField(blank=True, null=True)
    sentpkt = models.BigIntegerField(blank=True, null=True)
    rcvdpkt = models.BigIntegerField(blank=True, null=True)
    appcat = models.CharField(max_length=100, blank=True, null=True)
    crscore = models.CharField(max_length=11, blank=True, null=True)
    craction = models.CharField(max_length=11, blank=True, null=True)
    crlevel = models.CharField(max_length=50, blank=True, null=True)
    srchwvendor = models.CharField(max_length=100, blank=True, null=True)
    mastersrcmac = models.CharField(max_length=50, blank=True, null=True)
    srcmac = models.CharField(max_length=50, blank=True, null=True)
    srcserver = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'
        indexes = [
            models.Index(fields=['date']),  # Index for date
            models.Index(fields=['subtype']),  # Additional index example
        ]

    def __str__(self):
        return f'{self.date} ({self.time}) - {self.devname}'
    
class SystemConfiguration(models.Model):
    SYSTEM_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('server', 'Server'),
    ]
    
    system_name = models.CharField(max_length=222)
    system_type = models.CharField(max_length=6, choices=SYSTEM_TYPE_CHOICES)
    system_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)

    class Meta:
        db_table = 'system_configuration'
        constraints = [
            models.UniqueConstraint(fields=['system_name', 'system_ip'], name='unique_system_name_system_ip')
        ]

    def __str__(self):
        return f'{self.system_name} ({self.system_type}) - {self.system_ip}'

class SystemIPPool(models.Model):
    from_ip_range = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    to_ip_range = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, related_name='ip_pools')

    class Meta:
        db_table = 'system_ip_pool'

    def __str__(self):
        return f'IP Range: {self.from_ip_range} - {self.to_ip_range} (Department: {self.department})'


class Department(models.Model):
    department_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'departments'
    def __str__(self):
        return f"{self.department_name}"    