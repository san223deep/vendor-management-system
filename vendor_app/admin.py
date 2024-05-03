from django.contrib import admin
from .models import *


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_details', 'address', 'vendor_code')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'status', 'quality_rating', 'delivery_date',
                    'issue_date', 'acknowledgment_date', 'complete_cancel_date')
