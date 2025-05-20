from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 


class Currency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_item = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
    

class Offer(models.Model):
    
    
    class Status(models.TextChoices):
        OPEN = ('open', _('فعال'))
        CLOSED = ('closed', _('غیرفعال'))
        
        
    offered_by = models.ForeignKey(User, related_name="offers", on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, related_name="accepted", on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="open")
    title = models.CharField(max_length=120)
    description = models.TextField()
    to_give = models.ForeignKey(Currency, related_name="offers_to_give", on_delete=models.SET_NULL, null=True)
    to_get = models.ForeignKey(Currency, related_name="offers_to_get",  on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)