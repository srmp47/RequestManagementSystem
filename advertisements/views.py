from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import DynamicPermission

from .models import Advertisement
from .serializers import RequestSerializer, AllocateContractorSerializer


class RequestListCreateView(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or getattr(user, 'is_support', False):
            return Advertisement.objects.all()

        return Advertisement.objects.filter(
            Q(user=user) | ~Q(status=Advertisement.Status.CANCELED)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RequestRetrieveUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Advertisement.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if obj.user != user and not (
            user.is_staff or getattr(user, 'is_support', False)
        ):
            self.permission_denied(
                self.request,
                message="You do not have permission to modify this ad."
            )

        return obj


class CancelApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if request.user in advertisement.applicants.all():
            advertisement.applicants.remove(request.user)
            return Response(
                {"detail": "Application withdrawn successfully."}
            )

        return Response(
            {"detail": "You have not applied for this advertisement."},
            status=status.HTTP_400_BAD_REQUEST
        )


class AllocateContractorView(generics.GenericAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AllocateContractorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: RequestSerializer})
    def post(self, request, *args, **kwargs):
        advertisement = self.get_object()

        if advertisement.user != request.user:
            return Response(
                {"detail": "You do not own this advertisement."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contractor_id = serializer.validated_data['contractor_id']

        contractor = get_object_or_404(User, id=contractor_id)

        if contractor not in advertisement.applicants.all():
            return Response(
                {"detail": "User is not in applicants list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (
            getattr(contractor, 'is_contractor', False)
            or contractor.is_superuser
        ):
            return Response(
                {"detail": "Selected user is not a contractor."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                advertisement.contractor = contractor
                advertisement.status = Advertisement.Status.ALLOCATED
                advertisement.save()
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            RequestSerializer(advertisement).data,
            status=status.HTTP_200_OK
        )


class MarkAsDoneView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if advertisement.contractor != request.user:
            return Response(
                {"detail": "Only contractor can mark as done."},
                status=status.HTTP_403_FORBIDDEN
            )

        if advertisement.status != Advertisement.Status.ALLOCATED:
            return Response(
                {"detail": "Invalid advertisement status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.status = Advertisement.Status.PENDING_APPROVAL
        advertisement.save()
        return Response(
            {"detail": "Waiting for customer approval."}
        )


class ConfirmDoneView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if advertisement.user != request.user:
            return Response(
                {"detail": "Only owner can confirm completion."},
                status=status.HTTP_403_FORBIDDEN
            )

        if advertisement.status != Advertisement.Status.PENDING_APPROVAL:
            return Response(
                {"detail": "Task not marked as finished."},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.status = Advertisement.Status.DONE
        advertisement.save()
        return Response({"detail": "Task confirmed as DONE."})


class CancelAdvertisementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if advertisement.user != request.user:
            return Response(
                {"detail": "Only owner can cancel advertisement."},
                status=status.HTTP_403_FORBIDDEN
            )

        if advertisement.status in [
            Advertisement.Status.DONE,
            Advertisement.Status.CANCELED,
        ]:
            return Response(
                {"detail": "Advertisement cannot be canceled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.status = Advertisement.Status.CANCELED
        advertisement.save()
        return Response({"detail": "Advertisement canceled."})


class ContractorDailyScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if not getattr(user, 'is_contractor', False):
            return Response(
                {"detail": "Only contractors can view schedule."},
                status=status.HTTP_403_FORBIDDEN
            )

        date_str = request.query_params.get('date')
        if not date_str:
            return Response(
                {"detail": "date query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_date = parse_date(date_str)
        if target_date is None:
            return Response(
                {"detail": "Invalid date format (YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        jobs = Advertisement.objects.filter(
            contractor=user,
            execution_time__date=target_date,
            status=Advertisement.Status.ALLOCATED
        ).order_by('execution_time')

        return Response(RequestSerializer(jobs, many=True).data)


class ApplyForAdvertisementView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        DynamicPermission
    ]
    required_permission = 'can_apply_ads'

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if advertisement.user == request.user:
            return Response(
                {"detail": "You cannot apply to your own ad."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if advertisement.status != Advertisement.Status.OPEN:
            return Response(
                {"detail": "Advertisement is not OPEN."},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.applicants.add(request.user)
        return Response({"detail": "Applied successfully."})


class SetExecutionDetailsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        DynamicPermission
    ]
    required_permission = 'can_set_execution'

    class SetExecutionDetailsSerializer(serializers.Serializer):
        execution_time = serializers.DateTimeField()
        execution_location = serializers.CharField(max_length=255)

    def post(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        if advertisement.contractor != request.user:
            return Response(
                {"detail": "You are not assigned to this ad."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.SetExecutionDetailsSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        try:
            advertisement.execution_time = (
                serializer.validated_data['execution_time']
            )
            advertisement.execution_location = (
                serializer.validated_data['execution_location']
            )
            advertisement.full_clean()
            advertisement.save()
        except ValidationError as e:
            return Response(
                {"detail": e.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"detail": "Execution details updated."})
