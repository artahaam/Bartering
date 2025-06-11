from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from barter.models import Offer

class Rating(models.Model):

    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )
    
    rated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_ratings'
    )
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    review_text = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rater', 'rated_user', 'offer'], name='unique_rating_per_offer')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.score}-star rating by {self.rater} for {self.rated_user} on offer {self.offer.id}'
    
