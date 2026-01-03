from django.db import models
from django.conf import settings
from advertisements.models import Advertisement

class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        INVESTIGATING = "INVESTIGATING", "Under Investigation"
        CLOSED = "CLOSED", "Closed"

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    answer = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.sender.username}"