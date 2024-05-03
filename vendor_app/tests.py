from ddf import G
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.authtoken.models import Token
import json
from .models import Vendor, PurchaseOrder


class VendorTests(TestCase):

    def get_headers(self):
        user = G(User)
        token = G(Token, user=user)
        headers = {'Authorization': f'Token {token}'}
        return headers

    def test_vendor_crudl_view(self):

        data = {"name": "Vendor 1", "contact_details": "phone: +91000000000", "address": "yemen road, yemen"}
        headers = self.get_headers()
        vendor_cl_url = reverse('vendor_cl_view')

        # Testing vendor create view
        response_create = self.client.post(vendor_cl_url, data=data, headers=headers)
        self.assertEqual(response_create.status_code, 201)
        response_create_json = response_create.json()
        new_vendor_id = response_create_json['data']['id']

        # Testing vendor list view. Now vendor count should be 1
        response_list = self.client.get(vendor_cl_url, headers=headers)
        self.assertEqual(response_list.status_code, 200)
        response_list_json = response_list.json()
        self.assertEqual(len(response_list_json['data']), 1)

        vendor_rud_url = reverse('vendor_rud_view', args=(new_vendor_id,))

        # Testing vendor read view
        response_read = self.client.get(vendor_rud_url, headers=headers)
        self.assertEqual(response_read.status_code, 200)
        response_read_json = response_read.json()
        self.assertEqual(response_read_json['data']['name'], 'Vendor 1')

        # Testing vendor update view
        data_put = {'name': 'New Vendor'}
        response_put = self.client.put(vendor_rud_url, data=json.dumps(data_put), headers=headers,
                                       content_type='application/json')
        self.assertEqual(response_put.status_code, 200)

        # checking if name changed
        response_read = self.client.get(vendor_rud_url, headers=headers)
        response_read_json = response_read.json()
        self.assertEqual(response_read_json['data']['name'], 'New Vendor')

        # Testing vendor delete view
        response_delete = self.client.delete(vendor_rud_url, headers=headers)
        self.assertEqual(response_delete.status_code, 200)

        # Vendor count should be 0
        new_response_list = self.client.get(vendor_cl_url, headers=headers)
        new_response_list_json = new_response_list.json()
        self.assertEqual(len(new_response_list_json['data']), 0)


class PurchaseOrderTests(TestCase):
    def get_headers(self):
        user = G(User)
        token = G(Token, user=user)
        headers = {'Authorization': f'Token {token}'}
        return headers

    def test_order_crudl_view(self):

        data = {"items": {"phone": 2, "laptop": 3}}
        headers = self.get_headers()
        order_cl_url = reverse('order_cl_view')

        # Testing order create view
        response_create = self.client.post(order_cl_url, data=json.dumps(data), headers=headers,
                                           content_type='application/json')
        self.assertEqual(response_create.status_code, 201)
        response_create_json = response_create.json()
        self.assertEqual(response_create_json['data']['quantity'], 5)
        new_purchase_id = response_create_json['data']['id']

        # Testing order list view. Now vendor count should be 1
        response_list = self.client.get(order_cl_url, headers=headers)
        self.assertEqual(response_list.status_code, 200)
        response_list_json = response_list.json()
        self.assertEqual(len(response_list_json['data']), 1)

        order_rud_view = reverse('order_rud_view', args=(new_purchase_id,))

        # Testing vendor read view
        response_read = self.client.get(order_rud_view, headers=headers)
        self.assertEqual(response_read.status_code, 200)

        # Testing vendor update view
        # Make sure delivery_date is future date
        data_put = {"items": {"phone": 4, "laptop": 3}, "delivery_date": "2025-05-25"}
        response_put = self.client.put(order_rud_view, data=json.dumps(data_put), headers=headers,
                                       content_type='application/json')
        self.assertEqual(response_put.status_code, 200)

        # checking if quantity changed
        response_read = self.client.get(order_rud_view, headers=headers)
        response_read_json = response_read.json()
        self.assertEqual(response_read_json['data']['quantity'], 7)

        # Testing order delete view
        response_delete = self.client.delete(order_rud_view, headers=headers)
        self.assertEqual(response_delete.status_code, 200)

        # Vendor count should be 0
        new_response_list = self.client.get(order_rud_view, headers=headers)
        new_response_list_json = new_response_list.json()
        self.assertEqual(len(new_response_list_json['data']), 0)



