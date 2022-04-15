from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)             # Username should be String with maximum characters 15
    password = serializers.CharField(max_length=20)             # Password should be String with maximum characters 15

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)             # Username should be String with maximum characters 15
    password = serializers.CharField(max_length=20)             # Password should be String with maximum characters 15
    user_type = serializers.IntegerField()   