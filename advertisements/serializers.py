from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Advertisement

class RequestSerializer(serializers.ModelSerializer):
    # Nested or String representation of the user
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['date', 'status']  # Status usually changed by admins