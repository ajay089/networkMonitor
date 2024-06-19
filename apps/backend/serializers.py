from rest_framework import serializers

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
