from rest_framework import generics, permissions
from .models import Advertisement
from .serializers import RequestSerializer

# --- Request Views ---
class RequestListCreateView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user
        serializer.save(user=self.request.user)

class RequestRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

