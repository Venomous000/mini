from django.urls import path
from . import views

urlpatterns = [
    # User Order History & Management
    path('history/', views.order_history, name='order_history'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/', views.order_history, name='view_orders'),
    
    # Cart Checkout Flow
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/place/', views.place_cart_order, name='place_cart_order'),

    # Buy Now Flow
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('buy-now/checkout/', views.checkout_buy_now, name='checkout_buy_now'),
    path('buy-now/place/', views.place_buy_now_order, name='place_buy_now_order'),

    # Admin Order Views
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]
