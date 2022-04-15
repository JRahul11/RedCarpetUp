from rest_framework import serializers



class ValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=100)
    user_type = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    state = serializers.CharField(max_length=20)
    income_from_salary = serializers.IntegerField()
    income_from_shares = serializers.IntegerField()
    tax_status = serializers.IntegerField()