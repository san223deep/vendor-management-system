from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, \
    VendorOrderSerializer, UserSerializer, HistoricalPerformanceSerializer


class UserSignup(APIView):

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if email:
            token = Token.objects.filter(user__email=email).first()
            if token:
                message = 'success'
                data = {'auth_token': token.key}
                status_code = 200
            else:
                message = 'Email not registered. Call this url with post request and send email in request with key email'
                data = {}
                status_code = 400

        else:
            message = 'Please send email in query params.'
            data = {}
            status_code = 400

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            message = 'success'
            data = {'auth_token': token.key}
            status_code = 201
        else:
            message = 'failed'
            data = serializer.errors
            status_code = 400
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class VendorCLView(APIView):
    """
    Create and list view for Vendor.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.all()
        data = VendorSerializer(vendors, many=True).data
        message = 'success'
        status_code = 200
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'success'
            data = serializer.data
            status_code = 201
        else:
            message = 'failed'
            data = serializer.errors
            status_code = 400

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class VendorRUDView(APIView):
    """
    Read, update and delete view for Vendor.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(id=kwargs['vendor_id']).first()
        if vendor:
            message = 'success'
            data = VendorSerializer(vendor).data
            status_code = 200
        else:
            message = 'Vendor id does not exists'
            data = {}
            status_code = 404
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def put(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(id=kwargs['vendor_id']).first()
        a = request.data
        b = type(a)
        if vendor:
            serializer = VendorSerializer(instance=vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message = 'success'
                data = serializer.data
                status_code = 200
            else:
                message = 'failed'
                data = serializer.errors
                status_code = 400
        else:
            message = 'Vendor id does not exists'
            data = {}
            status_code = 404

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def delete(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(id=kwargs['vendor_id']).first()
        if vendor:
            vendor_code = vendor.vendor_code
            vendor.delete()
            message = f'Vendor {vendor_code} deleted successfully'
            data = {}
            status_code = 200
        else:
            message = 'Vendor id does not exists'
            data = {}
            status_code = 404

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class PurchaseOrderCLView(APIView):
    """
    Create and list view for PurchaseOrder.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
        else:
            orders = PurchaseOrder.objects.all()
        data = PurchaseOrderSerializer(orders, many=True).data
        message = 'success'
        status_code = 200
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'success'
            data = serializer.data
            status_code = 201
        else:
            message = 'failed'
            data = serializer.errors
            status_code = 400

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class PurchaseOrderRUDView(APIView):
    """
    Read, update and delete view for PurchaseOrder.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = PurchaseOrder.objects.filter(id=kwargs['po_id']).first()
        if order:
            message = 'success'
            data = PurchaseOrderSerializer(order).data
            status_code = 200
        else:
            message = 'order id does not exists'
            data = {}
            status_code = 404
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def put(self, request, *args, **kwargs):
        order = PurchaseOrder.objects.filter(id=kwargs['po_id']).first()
        if order:
            serializer = PurchaseOrderSerializer(instance=order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message = 'success'
                data = serializer.data
                status_code = 200
            else:
                message = 'failed'
                data = serializer.errors
                status_code = 400
        else:
            message = 'Order id does not exists'
            data = {}
            status_code = 404

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def delete(self, request, *args, **kwargs):
        order = PurchaseOrder.objects.filter(id=kwargs['po_id']).first()
        if order:
            po_number = order.po_number
            order.delete()
            message = f'Order {po_number} deleted successfully'
            data = {}
            status_code = 200
        else:
            message = 'Order id does not exists'
            data = {}
            status_code = 404

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class VendorPerformanceView(APIView):
    """
    Retrieve vendor performance.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(id=kwargs['vendor_id']).first()
        if vendor:
            message = 'success'
            data = VendorPerformanceSerializer(vendor).data
            status_code = 200
        else:
            message = 'Vendor id does not exists'
            data = {}
            status_code = 404
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class OrderIssueView(APIView):
    """
    Assign vendor to order.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        po_id = kwargs['po_id']
        serializer = VendorOrderSerializer(data=request.data, context={'po_id': po_id})
        if serializer.is_valid():
            order = PurchaseOrder.objects.filter(id=po_id).first()
            vendor = Vendor.objects.filter(id=serializer.validate_vendor_id(request.data['vendor_id'])).first()

            # Order should not be re-assigned to a vendor if it already has vendor and order has been acknowledged
            if order.vendor and order.acknowledgment_date:
                message = 'Last assigned vendor has acknowledged the vendor'
                status_code = 400
                data = {}
            else:
                order.vendor = vendor
                order.issue_date = timezone.now()
                order.save()
                message = f'order {po_id} has been assigned to {vendor.id}({vendor})'
                status_code = 200
                data = {}
        else:
            message = 'failed'
            status_code = 400
            data = serializer.errors
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class OrderAcknowledgeView(APIView):
    """
    Add acknowledgement time for order.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        po_id = kwargs['po_id']
        serializer = VendorOrderSerializer(data=request.data, context={'po_id': po_id})
        if serializer.is_valid():
            order = PurchaseOrder.objects.filter(id=po_id).first()
            vendor = Vendor.objects.get(id=serializer.validate_vendor_id(request.data['vendor_id']))
            if not order.vendor or order.vendor.id != vendor.id:
                message = 'Incorrect vendor id provided.'
                status_code = 400
                data = {}
            else:
                if order.acknowledgment_date:
                    message = 'Order already acknowledged'
                    status_code = 400
                    data = {}
                else:
                    order.acknowledgment_date = timezone.now()
                    order.save()
                    message = f'Vendor {vendor.id}({vendor}) has acknowledged order {po_id}'
                    status_code = 200
                    data = {}
        else:
            message = 'failed'
            status_code = 400
            data = serializer.errors
        response = {'message': message, 'data': data}
        return Response(response, status=status_code)


class OrderStatusChangeView(APIView):
    """
    Change status of purchase order to complete or cancel.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        po_id = kwargs['po_id']
        new_status = kwargs['new_status']
        order = PurchaseOrder.objects.filter(id=po_id).first()
        if order:
            # check if order is already closed (completed/canceled)
            if order.status in [PurchaseOrder.OrderStatus.completed, PurchaseOrder.OrderStatus.canceled]:
                return Response({'message': 'This order already has been closed.'}, status=200)

            if new_status == 'completed':
                order.status = PurchaseOrder.OrderStatus.completed
                if 'quality_rating' in request.data:
                    if request.data['quality_rating'] not in range(1, 6):
                        message = 'quality_rating should integer from 1-5'
                        status_code = 400
                        return Response({'message': message}, status=status_code)
                    else:
                        order.quality_rating = request.data['quality_rating']
            elif new_status == 'canceled':
                order.status = PurchaseOrder.OrderStatus.canceled
            else:
                return Response({'message': 'Invalid new_status value. Select completed or canceled.'}, status=400)
            order.complete_cancel_date = timezone.now()
            order.save()
            message = f"Order {order.id} has been marked {new_status}"
            status_code = 200
        else:
            message = f"Invalid order id"
            status_code = 404

        response = {'message': message}
        return Response(response, status=status_code)


class HistoricalPerformanceView(APIView):
    """
    Read/Create view for vendor historic performance
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            if vendor:
                date = request.query_params.get('date')
                if date:
                    try:
                        date = datetime.strptime(date, '%Y-%m-%d')
                    except:
                        message = 'Date should be in yyyy-mm-dd format'
                        return Response({'message': message}, status=400)
                    historic_data = HistoricalPerformance.objects.filter(Q(date=date) & Q(vendor=vendor)).first()
                    serializer_data = HistoricalPerformanceSerializer(historic_data).data
                else:
                    historic_data = HistoricalPerformance.objects.filter(vendor=vendor).first()
                    serializer_data = HistoricalPerformanceSerializer(historic_data, many=True).data

                message = 'success'
                data = serializer_data
                status_code = 200
            else:
                message = 'incorrect vendor id'
                data = {}
                status_code = 404

        else:
            message = 'Please add vendor_id query_params'
            data = {}
            status_code = 404

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        serializer = HistoricalPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'success'
            data = serializer.data
            status_code = 201
        else:
            message = 'fail'
            data = serializer.errors
            status_code = 400

        response = {'message': message, 'data': data}
        return Response(response, status=status_code)