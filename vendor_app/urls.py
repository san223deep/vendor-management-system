from django.urls import path
from . import views


urlpatterns = [
    path('user/signup/', views.UserSignup.as_view()),
    path('vendors/', views.VendorCLView.as_view(), name='vendor_cl_view'),
    path('vendors/<vendor_id>/', views.VendorRUDView.as_view(), name='vendor_rud_view'),
    path('purchase_orders/', views.PurchaseOrderCLView.as_view(), name='order_cl_view'),
    path('purchase_orders/<po_id>/', views.PurchaseOrderRUDView.as_view(), name='order_rud_view'),
    path('vendors/<vendor_id>/performance/', views.VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/<po_id>/issue/', views.OrderIssueView.as_view(), name='issue_order'),
    path('purchase_orders/<po_id>/acknowledge/', views.OrderAcknowledgeView.as_view(), name='acknowledge_order'),
    path('purchase_orders/<po_id>/change_status/<new_status>/', views.OrderStatusChangeView.as_view(),
         name='change_order_status'),
    path('historic_performance/', views.HistoricalPerformanceView.as_view(), name='historic_performance')
]
