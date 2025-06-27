from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.user_home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Admin
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin/products/<int:product_id>/upload-image/', views.upload_product_image, name='upload_product_image'),
    path('admin/products/delete-image/<int:image_id>/', views.delete_product_image, name='admin_delete_product_image'),

    path('admin/categories/add/', views.add_category, name='add_category'),
    path('admin/categories/delete/<int:category_id>/', views.delete_category, name='admin_delete_category'),
    path('admin/categories/edit/<int:category_id>/', views.edit_category, name='admin_edit_category'),

]
