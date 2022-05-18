from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Dishes
from datetime import datetime
import logging


@receiver(pre_save, sender=Dishes)
def is_active_off(sender, instance, **kwargs):
    print('-' * 20)
    logging.warning('Блюдо "{dish}", "is_active" = {status}, дата {data}'.
                    format(dish=instance.title,
                           data=datetime.today(),
                           status=instance.is_active))
    print('-' * 20)
