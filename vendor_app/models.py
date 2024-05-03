import random
from django.db import models
from model_utils import FieldTracker


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=9, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            while True:
                code = f"VC{random.randint(1000000, 9999999)}"
                if not Vendor.objects.filter(vendor_code=code).exists():
                    self.vendor_code = code
                    break
        super(Vendor, self).save(*args, **kwargs)


class PurchaseOrder(models.Model):
    class OrderStatus(models.TextChoices):
        pending = 'P', 'Pending'
        completed = 'c', 'Completed'
        canceled = 'ca', 'Canceled'

    po_number = models.CharField(max_length=9, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, related_name='purchase_orders',
                               null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.pending)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    complete_cancel_date = models.DateTimeField(null=True, blank=True)
    tracker = FieldTracker()

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if not self.po_number:
            while True:
                po_number = f"PO{random.randint(1000000, 9999999)}"
                if not PurchaseOrder.objects.filter(po_number=po_number).exists():
                    self.po_number = po_number
                    break
        self.quantity = sum([i for i in self.items.values()])
        super(PurchaseOrder, self).save(*args, **kwargs)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='performance')
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} performance: {self.date.date}"
