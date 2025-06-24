from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Superadmin Routes
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin/products/<int:product_id>/upload-image/', views.upload_product_image, name='upload_product_image'),
    path('admin/categories/add/', views.add_category, name='add_category'),
]

