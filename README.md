# Vendor Management System

This project is a Vendor Management System built using Django and Django REST Framework. The system manages vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [API Endpoints](#api-endpoints)
3. [Testing](#testing)


## Setup Instructions

1. **Clone the Repository**

   ```
   git clone https://github.com/san223deep/vendor-management-system.git
   ```
2. **Virtual environment setup**

   ```
   python3 -m venv env_vendor
   source env_vendor/bin/activate (on ubuntu)
   env_vendor/scripts/activate (on windows)
   ```
3. **Install Dependencies**

   ```
   cd vendor-management-system
   pip3 install -r requirements.txt
   ```
4. **Apply Migrations**
   
   ```
   python3 manage.py migrate
   ```

5. **Run the Server**

   ```
   python manage.py runserver
   ```
   Base url will be `http://127.0.0.1:8000`

## API Endpoints
**<u>Note</u>**: fields with * are required fields. Do not add * with fields in payload.
1. **Generate auth token**

   Use this endpoint to register user.

   - `POST /api/user/signup/`:  `email*(email field)`
   
   This will return auth token in response. Send auth token in header with every endpoint in following format otherwise it will return not authorized error.
   `{'Authorization': 'Token <auth_token>'}`


2. **Vendor Endpoints**
   
   - `POST /api/vendors/`: Add new vendor (name*, contact_details*, address*)
   - `GET /api/vendors/`:  List all vendors
   - `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details
   - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details (name, contact_details, address)
   - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor
   

3. **Purchase Order Endpoints**

   - `POST /api/purchase_orders/`: Create a purchase order (items*, delivery_date)
   
      <u><i>Note</i></u>: `items` should be json like `{"items": {"phone": 2, "laptop": 3}}` and `delivery_date` is 
     optional and should be in `yyyy-mm-dd` format
  
   - `GET /api/purchase_orders/`:  List all purchase orders. Send `vendor_id` in query params to filter by vendor
   - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order
   - `PUT /api/purchase_orders/{po_id}`: Update a purchase order (items, delivery_date)
   - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order
   
 
4. **Performance Endpoints**
   - `GET /api/vendors/{vendor_id}/performance/`: Retrieve a vendor's performance metrics
   - `POST /api/purchase_orders/<po_id>/issue/`: Assign order to vendor (vendor_id*)
   - `POST /api/purchase_orders/{po_id}/acknowledge`: Acknowledge order by vendor (vendor_id)
   - `GET /api/historic_performance/`: Get vendor daily performance. send vendor_id(required) in query_params for specific. 
   send date (yyyy-mm-dd) for performance on specific date
   - `POST /api/historic_performance/`  Add performance for specific date (on_time_delivery_rate*(float), quality_rating_avg*(float),
     average_response_time*(float),fulfillment_rate*(float), date, vendor)
     
## Testing
Tests are written in `vendor_app/tests.py`. Use command `pytest` in shell to run all the tests

   
