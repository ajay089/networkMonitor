from rest_framework import serializers
from apps.frontend.models import (
    SystemConfiguration, SystemIPPool
)

class DashboardDataSerializer(serializers.Serializer):
    totalCountToday = serializers.IntegerField()
    totalCountYesterday = serializers.IntegerField()
    totalOutgoingToday = serializers.IntegerField()
    totalOutgoingYesterday = serializers.IntegerField()
    totalIncomingToday = serializers.IntegerField()
    totalIncomingYesterday = serializers.IntegerField()
    loginAttemptsToday = serializers.IntegerField()
    loginAttemptsYesterday = serializers.IntegerField()
    isTotalCountGreater = serializers.BooleanField()
    isTotalOutgoingGreater = serializers.BooleanField()
    isTotalIncomingGreater = serializers.BooleanField()
    isLoginAttemptsGreater = serializers.BooleanField()
    pctChangeTotalCount = serializers.FloatField(allow_null=True)
    pctChangeTotalOutgoing = serializers.FloatField(allow_null=True)
    pctChangeTotalIncoming = serializers.FloatField(allow_null=True)
    pctChangeLoginAttempts = serializers.FloatField(allow_null=True)

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = ['id', 'system_name', 'system_type', 'system_ip']

class PaginatedSystemConfigurationSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = SystemConfigurationSerializer(many=True)
    current_page = serializers.SerializerMethodField()
    page_size = serializers.IntegerField()
    system_name = serializers.CharField(allow_blank=True)

    def get_current_page(self, obj):
        if 'request' in self.context:
            return int(self.context['request'].query_params.get('page', 1))
        return 

class SystemIpPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemIPPool
        fields = ['id', 'from_ip_range', 'to_ip_range']

class PaginatedSystemIpPoolSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = SystemIpPoolSerializer(many=True)
    current_page = serializers.SerializerMethodField()
    page_size = serializers.IntegerField()

    def get_current_page(self, obj):
        if 'request' in self.context:
            return int(self.context['request'].query_params.get('page', 1))
        return 1    
