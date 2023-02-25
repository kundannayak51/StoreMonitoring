from django.db.models.signals import pre_save
from django.dispatch import receiver

from monitor.constants import DEFAULT_TIMEZONE
from monitor.models import StoreBusinessHours, Store


@receiver(pre_save, sender=StoreBusinessHours)
def create_timezone_if_not_exists(sender, instance, **kwargs):
    # Check if a Store object with the specified store_id already exists in the Timezones table
    try:
        Store.objects.get(store_id=instance.store_id)
    except Store.DoesNotExist:
        Store.objects.create(store_id=instance.store_id, timezone_str=DEFAULT_TIMEZONE)
