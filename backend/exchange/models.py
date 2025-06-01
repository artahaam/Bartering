from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings

class Currency(models.Model):
    
    class Meta:
        verbose_name = _('واحد تبادل')
        verbose_name_plural = _('واحدهای تبادل')
        db_table = 'currencies'
        managed = False
    
    
    name = models.CharField(_('نام'), max_length=100)
    description = models.TextField(_('توضیحات'), blank=True)
    is_item = models.BooleanField(_('کالا'), default=True)
    is_service = models.BooleanField(_('خدمات'), default=False)
    
    
    def __str__(self):
        return self.name


class Offer(models.Model):
    class Meta:
        verbose_name = _('آگهی')
        verbose_name_plural = _('آگهی‌ها')
        db_table = 'offers'
        managed = False
    
    
    class Status(models.TextChoices):
        OPEN = ('open', _('فعال'))
        DONE = ('matched', _('انجام شده'))
        CLOSED = ('closed', _('غیرفعال'))
        
    offered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="offers",
                                   on_delete=models.CASCADE,
                                   verbose_name=_('پیشنهاد دهنده'),
                                   null=True,
                                   db_column="offered_by",
                                   )
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="accepted_by",
                                    on_delete=models.SET_NULL,
                                    verbose_name=_('پذیرنده'),
                                    null=True,
                                    blank=True,
                                    db_column="accepted_by",
                                    )
    status = models.CharField(_('وضعیت'), max_length=20, choices=Status, default=Status.OPEN)
    title = models.CharField(_('عنوان'), max_length=120)
    description = models.TextField(_('توضیحات'))
    
    to_get = models.ForeignKey(Currency,
                               related_name="offers_to_get",
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name=_('تقاضا'),
                               db_column='to_get',
                               )
    
    to_give = models.ForeignKey(Currency,
                                related_name="offers_to_give",
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name=_('عرضه'),
                                db_column='to_give'
                                )
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)

    def __str__(self):
        return self.title


class OfferProposal(models.Model):
    class Meta:
        verbose_name = _('پیشنهاد آگهی')
        verbose_name_plural = _('پیشنهادهای آگهی')
        db_table = 'offer_proposal'
    
    
    offer_id = models.ForeignKey(Offer,
                                 db_column="offer_id",
                                 on_delete=models.CASCADE,
                                 related_name="proposals",
                                 null=True,
                                 blank=True,
                                 verbose_name=_('شماره آگهی'))
    
    
    proposer_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    db_column="proposer_id",
                                    on_delete=models.CASCADE,
                                    verbose_name=_('متقاضی'),
                                    null=True,
                                    blank=True,
                                    )
    
    
    proposed_currency = models.ForeignKey(Currency,
                                        db_column="proposed_currency",
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        verbose_name=_('واحد پیشنهادی'))
    
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.proposer} on {self.offer_id}"