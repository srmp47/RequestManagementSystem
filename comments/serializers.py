from rest_framework import serializers
from .models import Comment, Review
from advertisements.models import Advertisement


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = [
            'id',
            'request',
            'user',
            'user_name',
            'rating',
            'content',
        ]
        read_only_fields = ['user']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def validate(self, data):
        ad_id = self.context['view'].kwargs.get('pk')
        if not ad_id:
            raise serializers.ValidationError(
                "Advertisement id is required."
            )

        try:
            advertisement = Advertisement.objects.get(pk=ad_id)
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError(
                "Advertisement not found."
            )

        if advertisement.status != Advertisement.Status.DONE:
            raise serializers.ValidationError(
                "Reviews allowed only for DONE advertisements."
            )

        if Review.objects.filter(
            advertisement=advertisement
        ).exists():
            raise serializers.ValidationError(
                "Review already exists for this advertisement."
            )

        return data
