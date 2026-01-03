from rest_framework.validators import UniqueValidator
import re
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from advertisements.models import Advertisement
from rest_framework import serializers
from django.db.models import Avg
from .models import User
from comments.models import Review

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

class ContractorProfileSerializer(serializers.ModelSerializer):
    completed_ads_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'completed_ads_count', 'average_rating', 'reviews']

    def get_completed_ads_count(self, obj):
        return Advertisement.objects.filter(contractor=obj, status='DONE').count()

    def get_average_rating(self, obj):
        avg = Review.objects.filter(contractor=obj).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def get_reviews(self, obj):
        from comments.serializers import ReviewSerializer
        reviews = Review.objects.filter(contractor=obj).order_by('-created_at')
        return ReviewSerializer(reviews, many=True).data




class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    created_ads = serializers.SerializerMethodField()
    completed_jobs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'first_name', 'last_name',
            'created_ads', 'completed_jobs'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_created_ads(self, obj):
        from advertisements.serializers import RequestSerializer
        ads = Advertisement.objects.filter(user=obj).order_by('-date')
        return RequestSerializer(ads, many=True).data

    def get_completed_jobs(self, obj):
        jobs = Advertisement.objects.filter(contractor=obj, status='DONE').order_by('-date')
        return RequestSerializer(jobs, many=True).data

