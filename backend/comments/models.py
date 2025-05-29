from django.db import models
from exchange.models import Offer
# from accounts.models import 
from django.conf import settings
from django.utils.translation import gettext_lazy as _ 

class Comment(models.Model):
    
    class Meta:
        verbose_name = _('نظر')
        db_table = 'comments'
        managed = False
    
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  verbose_name=_('نویسنده'),
                                  db_column='author_id',
                                  )
    
    parent_id = models.ForeignKey("self",
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE,
                                  verbose_name=_(''),
                                  db_column='parent_id',
                                  )
    
    text = models.TextField(_('متن'))
    created_at = models.DateTimeField(_('ساخته شده در'), auto_now_add=True)