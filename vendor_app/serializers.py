from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already registered")
        return email

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(username=email, email=email)
        user.set_password(email)
        return user


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields = ['id', 'vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    formatted_delivery_date = serializers.SerializerMethodField(read_only=True)
    issue_date = serializers.SerializerMethodField()
    acknowledgment_date = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['id', 'po_number', 'vendor', 'order_date', 'quantity', 'status',
                            'quality_rating', 'issue_date', 'acknowledgment_date']

    def get_status(self, obj):
        return obj.get_status_display()

    def get_order_date(self, obj):
        return obj.order_date.strftime("%B %d, %Y %I:%M:%S %p")

    def get_formatted_delivery_date(self, obj):
        return obj.delivery_date.strftime("%B %d, %Y %I:%M:%S %p") if obj.delivery_date else None

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # Move the value from `formatted_delivery_date` to `delivery_date` for response
        response['delivery_date'] = response.pop('formatted_delivery_date', None)
        return response

    def get_issue_date(self, obj):
        return obj.issue_date.strftime("%B %d, %Y %I:%M:%S %p") if obj.issue_date else None

    def get_acknowledgment_date(self, obj):
        return obj.acknowledgment_date.strftime("%B %d, %Y %I:%M:%S %p") if obj.acknowledgment_date else None

    def validate_delivery_date(self, delivery_date):
        tomorrow = timezone.now() + timedelta(days=1)
        if delivery_date < tomorrow:
            raise serializers.ValidationError("delivery_date cannot be before tomorrow")

        return delivery_date


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class VendorOrderSerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()

    def validate_vendor_id(self, vendor_id):
        po_id = self.context['po_id']
        order = PurchaseOrder.objects.filter(id=po_id).first()
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not order:
            raise serializers.ValidationError("Incorrect order id")

        if not vendor:
            raise serializers.ValidationError("Incorrect vendor id")

        return vendor_id


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
