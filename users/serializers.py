from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            EmailValidator(message="invalid email format"),
            UniqueValidator(queryset=User.objects.all(), message="This email is already registered.")
        ]
    )

    # برای شماره تلفن هم همین کار را انجام دهید
    phone = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This phone number is already registered.")
        ]
    )
    # استفاده از Validator پیش‌فرض برای ایمیل
    email = serializers.EmailField(validators=[EmailValidator(message="invalid email format")])

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    # ۱. چک کردن قدرت رمز عبور (Password Strength)
    def validate_password(self, value):
        # از اعتبارسنجی‌های داخلی جنگو استفاده می‌کند (طول، عددی نبودن و غیره)
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    # ۲. چک کردن فرمت شماره تماس (Regex)
    def validate_phone(self, value):
        # الگوی شماره موبایل ایران
        pattern = r'^09\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone number must be 11-digit number and starts with 09")
        return value

    # ۳. متد ذخیره‌سازی (که قبلاً اصلاح کردیم)
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, help_text="username, phone number or email")
    password = serializers.CharField(required=True, write_only=True)