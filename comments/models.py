from django.db import models
from advertisements.models import Advertisement
from users.models import User

class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
        verbose_name='Rating'
    )
    content = models.TextField()
    request = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)