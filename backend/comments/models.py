from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from barter.models import Offer

class Comment(models.Model):

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'Comment by {self.author} on offer {self.offer.id}'