from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
from datetime import timedelta

class Advertisement(models.Model):
    class Category(models.TextChoices):
        IT = "IT", "IT"
        HR = "HR", "HR"
        FINANCE = "Finance", "Finance"
        TECHNICAL = "TECHNICAL", "Technical"
        SERVICE = "SERVICE", "Service"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ALLOCATED = "ALLOCATED", "Allocated"
        PENDING_APPROVAL = "PENDING_APPROVAL", "Pending Approval"
        DONE = "DONE", "Done"
        CANCELED = "CANCELED", "Canceled"

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.IT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_ads')
    applicants = models.ManyToManyField(User, related_name='applied_ads', blank=True)
    execution_time = models.DateTimeField(null=True, blank=True)
    execution_location = models.CharField(max_length=255, null=True, blank=True)

    contractor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='allocated_jobs'
    )

    def clean(self):
        if self.contractor and self.execution_time:
            start_time = self.execution_time
            end_time = self.execution_time + timedelta(hours=2)

            overlapping_jobs = Advertisement.objects.filter(
                contractor=self.contractor,
                execution_time__lt=end_time,
                execution_time__gt=start_time - timedelta(hours=2)
            ).exclude(pk=self.pk)

            if overlapping_jobs.exists():
                raise ValidationError("This contractor already has a scheduled job that overlaps with this time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"