from datetime import datetime
from django.db.models import Avg, F, Q
from .models import Vendor, PurchaseOrder


def calculate_on_time_delivery_rate(po_id):
    """
    Calculate  on_time_delivery_rate for vendor.
    """
    order = PurchaseOrder.objects.filter(id=po_id).first()
    if order:
        vendor = order.vendor
        on_time_orders = PurchaseOrder.objects.filter(Q(complete_cancel_date__lte=F('delivery_date')) &
                                                      Q(vendor=vendor)).count()
        all_delivered_orders = PurchaseOrder.objects.filter(Q(status=PurchaseOrder.OrderStatus.completed) &
                                                            Q(vendor=vendor)).count()
        print(on_time_orders, all_delivered_orders)
        try:
            vendor.on_time_delivery_rate = round(on_time_orders/all_delivered_orders, 2)
        except ZeroDivisionError:
            vendor.on_time_delivery_rate = 0.0
        vendor.save()


def calculate_quality_rating_avg(vendor_id):
    """
    Calculate  quality_rating_avg for vendor.
    """
    vendor = Vendor.objects.filter(id=vendor_id).annotate(avg_quality=Avg('purchase_orders__quality_rating')).first()
    if vendor:
        vendor.quality_rating_avg = round(vendor.avg_quality, 2)
        vendor.save()


def calculate_average_response_time(vendor_id):
    """
    Calculate  average_response_time for vendor
    """
    vendor = Vendor.objects.filter(id=vendor_id).annotate(
        avg_time=Avg(F('purchase_orders__acknowledgment_date') - F('purchase_orders__issue_date'))).first()
    if vendor:
        vendor.average_response_time = round(vendor.avg_time.seconds/60, 2)
        vendor.save()


def calculate_fulfillment_rate(po_id):
    order = PurchaseOrder.objects.filter(id=po_id).first()
    if order:
        vendor = order.vendor
        all_delivered_orders = PurchaseOrder.objects.filter(Q(status=PurchaseOrder.OrderStatus.completed) &
                                                            Q(vendor=vendor)).count()
        closed_orders = [PurchaseOrder.OrderStatus.completed, PurchaseOrder.OrderStatus.canceled]
        now = datetime.now()

        # Filtering all completed/canceled orders or pending order for which delivery date is passed
        all_issued_orders = PurchaseOrder.objects.filter((Q(status__in=closed_orders) | Q(delivery_date__lt=now)) &
                                                         Q(vendor=vendor)).count()

        try:
            vendor.fulfillment_rate = round(all_delivered_orders/all_issued_orders, 2)
        except ZeroDivisionError:
            vendor.fulfillment_rate = 0.0

        vendor.save()
