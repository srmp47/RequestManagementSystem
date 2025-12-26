from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

import re
from rest_framework import serializers
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'validators': [
                    EmailValidator(message="invalid email format"),
                    UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")
                ]
            },
            'phone': {
                'validators': [
                    UniqueValidator(queryset=User.objects.all(), message="This phone number is already registered.")
                ]
            }
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate_phone(self, value):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone number must be 11-digit and start with 09")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, help_text="username, phone number or email")
    password = serializers.CharField(required=True, write_only=True)