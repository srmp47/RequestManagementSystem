from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import generics, permissions

from users.permissions import DynamicPermission
from .models import Ticket
from .serializers import TicketSerializer

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'is_support', False):
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(sender=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
class TicketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    def get_queryset(self):
        if self.request.user.is_support or self.request.user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(sender=self.request.user)
from rest_framework import generics, permissions
from .models import Ticket
from .serializers import TicketAnswerSerializer
from drf_spectacular.utils import extend_schema

class TicketAnswerView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketAnswerSerializer
    # به جای IsAdminUser، از دسترسی پویا استفاده می‌کنیم
    permission_classes = [permissions.IsAuthenticated, DynamicPermission]
    required_permission = 'can_answer_tickets'

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class AdminTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Ticket.objects.all().order_by('-created_at')