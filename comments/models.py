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


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from advertisements.models import Advertisement


class Review(models.Model):
    advertisement = models.OneToOneField(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.contractor.username} - Rating: {self.rating}"