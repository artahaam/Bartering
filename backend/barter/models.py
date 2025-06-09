from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings

class Tradeable(models.Model):
    
    class Meta:
        verbose_name = _('واحد تبادل')
        verbose_name_plural = _('واحدهای تبادل')
    
    
    class Type(models.TextChoices):
        ITEM = ('item', _('کالا'))
        SERVICE = ('service', _('خدمات'))
    
    
    name = models.CharField(_('نام'), max_length=100)
    description = models.TextField(_('توضیحات'), blank=True)
    type = models.CharField(_('کالا'), max_length=15, choices=Type, default=Type.ITEM)
    
    
    def __str__(self):
        return self.name


class Offer(models.Model):

    class Meta:
        verbose_name = _('آگهی')
        verbose_name_plural = _('آگهی‌ها')
    
    
    class Status(models.TextChoices):
        OPEN = ('open', _('فعال'))
        DONE = ('matched', _('انجام شده'))
        CLOSED = ('closed', _('غیرفعال'))
        
        
    offered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="offers",
                                   on_delete=models.CASCADE,
                                   verbose_name=_('پیشنهاد دهنده'),
                                   )
    
    
    status = models.CharField(_('وضعیت'), max_length=20,
                              choices=Status,
                              default=Status.OPEN
                              )
    
    title = models.CharField(_('عنوان'), max_length=120)
    description = models.TextField(_('توضیحات'))
    to_get = models.OneToOneField(Tradeable,
                               related_name="offers_to_get",
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name=_('تقاضا'),
                               )
    
    to_give = models.OneToOneField(Tradeable,
                                related_name="offers_to_give",
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name=_('عرضه'),
                                )
    
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)

    def __str__(self):
        return self.title


class Proposal(models.Model):
    
    class Meta:
        verbose_name = _('پیشنهاد آگهی')
        verbose_name_plural = _('پیشنهادهای آگهی')
    

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('انتظار')
        ACCEPTED = 'ACCEPTED', _('پذیرفته شده')
        DECLINED = 'DECLINED', _('رد شده')


    offer = models.ForeignKey(Offer,
                                 on_delete=models.CASCADE,
                                 related_name="proposals",
                                 verbose_name=_('شماره آگهی'))
    
    proposer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    verbose_name=_('متقاضی'),
                                    )
    
    proposed_tradeable = models.OneToOneField(Tradeable,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        verbose_name=_('واحد پیشنهادی'))
    
    status = models.CharField(_('وضعیت'), max_length=20,
                              choices=Status,
                              default=Status.PENDING,
                              )
    
    created_at = models.DateTimeField(_('ایجاد شده در'), auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.proposer} on {self.offer_id}"