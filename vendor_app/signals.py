from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .tasks import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, \
    calculate_fulfillment_rate


@receiver(post_save, sender=PurchaseOrder)
def purchase__order_post_save_operations(sender, **kwargs):
    instance = kwargs['instance']
    # previous value check has been added to avoid infinite loop when instance is saved in function called
    # from post_save

    if instance.tracker.has_changed('status') and instance.status == PurchaseOrder.OrderStatus.completed:
        # calls on status change and new status is completed
        calculate_on_time_delivery_rate(instance.id)
        calculate_fulfillment_rate(instance.id)

    if instance.tracker.has_changed('status') and instance.status == PurchaseOrder.OrderStatus.completed and \
       instance.tracker.has_changed('quality_rating'):
        # calls on status change and new status is completed and quality rating is provided
        calculate_quality_rating_avg(instance.vendor.id)

    if instance.tracker.has_changed('acknowledgment_date'):
        # calls when acknowledgment_date is changed
        calculate_average_response_time(instance.vendor.id)
