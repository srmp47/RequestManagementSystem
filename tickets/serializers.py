from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'message', 'answer', 'request', 'status']
        read_only_fields = ['id', 'answer', 'status']