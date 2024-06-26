from rest_framework import serializers
from apps.backend.models import (
    SystemConfiguration, SystemIPPool,
    Logs, Department
)
from datetime import datetime

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

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class SystemIpPoolSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = SystemIPPool
        fields = ['id', 'department', 'from_ip_range', 'to_ip_range']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = DepartmentSerializer(instance.department).data
        return representation

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

class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Assuming the date field in your model is called 'date'
        if 'date' in representation:
            # Format the date field to the desired format, e.g., 'YYYY-MM-DD'
            representation['date'] = datetime.strptime(representation['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        return representation

class PaginatedLogsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = LogsSerializer(many=True)
    current_page = serializers.SerializerMethodField()
    page_size = serializers.IntegerField()

    def get_current_page(self, obj):
        if 'request' in self.context:
            return int(self.context['request'].query_params.get('page', 1))
        return 1        
