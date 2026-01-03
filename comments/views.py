from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics, permissions
from .serializers import ReviewSerializer
from advertisements.models import Advertisement

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]





class SubmitReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad = Advertisement.objects.get(pk=self.kwargs['pk'])

        if ad.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the customer of this ad can leave a review.")

        serializer.save(
            advertisement=ad,
            author=self.request.user,
            contractor=ad.contractor
        )


from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer


from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

class ContractorReviewListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='rating',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter reviews by rating (1-5)',
                enum=[1, 2, 3, 4, 5]
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        contractor_id = self.kwargs['contractor_id']
        return Comment.objects.filter(request__contractor_id=contractor_id)