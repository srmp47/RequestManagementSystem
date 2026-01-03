from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from .serializers import ContractorProfileSerializer
from rest_framework import  filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .filters import ContractorFilter
from rest_framework import  permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import User
from .serializers import UserProfileSerializer
from drf_spectacular.utils import extend_schema


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['identifier'],
                password=serializer.validated_data['password']
            )

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username
                }, status=status.HTTP_200_OK)

            return Response({"detail": "input data is not valid"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ContractorProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ContractorProfileSerializer
    permission_classes = [AllowAny]



@extend_schema(tags=['Profiles'])
class PublicProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(tags=['Contractors'])
class ContractorListView(generics.ListAPIView):
    serializer_class = ContractorProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ContractorFilter

    ordering_fields = ['avg_rating', 'rev_count']

    ordering = ['-avg_rating']

    def get_queryset(self):
        return User.objects.annotate(
            avg_rating=Avg('reviews_received__rating'),
            rev_count=Count('reviews_received')
        ).filter(rev_count__gt=0)