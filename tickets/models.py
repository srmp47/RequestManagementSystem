from django.db import models

from requests.models import Request


class Ticket(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        Closed = "Closed", "Closed"
        REJECTED = "Rejected", "Rejected"
    message = models.TextField()
    answer = models.TextField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
