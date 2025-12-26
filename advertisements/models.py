from django.db import models
from users.models import User

class Advertisement(models.Model):
    class Category(models.TextChoices):
        IT = "IT", "IT"
        HR = "HR", "HR"
        FINANCE = "Finance", "Finance"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ALLOCATED = "ALLOCATED", "Allocated"
        DONE = "DONE", "Done"
        CANCELED = "CANCELED", "Canceled"

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.IT
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.status})"
