from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.place_order, name='place_order'),
    path('history/', views.order_history, name='order_history'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),

    # Admin URLs
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),

    # Buy Now URLs
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('buy-now/checkout/', views.checkout_buy_now, name='checkout_buy_now'),
    path('buy-now/place/', views.place_buy_now_order, name='place_buy_now_order'),

    # checkout URLs
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/place/', views.place_cart_order, name='place_cart_order'),
]
