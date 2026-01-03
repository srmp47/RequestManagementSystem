from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Advertisement
from users.models import User




class RequestSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    applicant_count = serializers.IntegerField(source='applicants.count', read_only=True)


    class Meta:
        model = Advertisement
        fields = [
        'id', 'title', 'content', 'category', 'status',
        'date', 'user', 'user_detail', 'applicants', 'applicant_count'
        ]
        read_only_fields = ['date', 'status', 'user', 'applicants']




class AllocateContractorSerializer(serializers.Serializer):
    contractor_id = serializers.IntegerField()


    def validate_contractor_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")


        if not (getattr(user, 'is_contractor', False) or user.is_superuser):
            raise serializers.ValidationError("Selected user is not a contractor.")
        return value