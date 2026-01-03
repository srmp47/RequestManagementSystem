
from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'sender', 'advertisement', 'title', 'message', 'answer', 'status', 'created_at']
        read_only_fields = ['sender', 'answer', 'status', 'created_at']

class TicketAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['answer']

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.answer)
        instance.status = Ticket.Status.CLOSED
        instance.save()
        return instance