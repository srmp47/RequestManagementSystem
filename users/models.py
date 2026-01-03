from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_contractor = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        permissions = [
            ("can_apply_ads", "Can apply for ads"),
            ("can_answer_tickets", "Can answer support tickets"),
            ("can_set_execution", "Can set time and place for work"),
        ]
