from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 


class Currency(models.Model):
    
    class Meta:
        verbose_name = _('واحد تبادل')
        db_table = 'currencies'
        managed = False
    
    
    name = models.CharField(_('نام'), max_length=100)
    description = models.TextField(_('توضیحات'), blank=True)
    is_item = models.BooleanField(_('کالا'), default=True)
    is_service = models.BooleanField(_('خدمات'), default=False)
    

class Offer(models.Model):
    class Meta:
        verbose_name = _('آگهی')
        db_table = 'offers'
        managed = False
    
    
    class Status(models.TextChoices):
        OPEN = ('open', _('فعال'))
        DONE = ('matched', _('انجام شده'))
        CLOSED = ('closed', _('غیرفعال'))
        
    offered_by = models.ForeignKey(User, related_name="offers", on_delete=models.CASCADE, verbose_name=_('پیشنهاد دهنده'), null=True)
    accepted_by = models.ForeignKey(User, related_name="accepted", on_delete=models.SET_NULL, verbose_name=_('پذیرنده'), null=True)
    status = models.CharField(_('وضعیت'), max_length=20, choices=Status, default=Status.OPEN)
    title = models.CharField(_('عنوان'), max_length=120)
    description = models.TextField(_('توضیحات'))
    to_give = models.ForeignKey(Currency, related_name="offers_to_give", on_delete=models.SET_NULL, null=True, verbose_name=_('عرضه'))
    to_get = models.ForeignKey(Currency, related_name="offers_to_get",  on_delete=models.SET_NULL, null=True, verbose_name=_('تقاضا'))
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)


class OfferProposal(models.Model):
    
    class Meta:
        verbose_name = _('آگهی‌های داری متقاضی')
        db_table = 'offer_proposal'
        managed = False
    
    
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="proposals", verbose_name=_('شماره آگهی'))
    proposer_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('متقاضی'))
    proposed_currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('واحد پیشنهادی'))
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)

