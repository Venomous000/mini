from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('superadmin/login/', views.superadmin_login_view, name='superadmin_login'),
    path('superadmin/logout/', views.superadmin_logout_view, name='superadmin_logout'),
    path('superadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('home/', views.user_home, name='user_home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/addresses/', views.manage_addresses, name='manage_addresses'),
    path('profile/addresses/add/', views.add_address, name='add_address'),
    path('profile/addresses/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('profile/addresses/delete/<int:address_id>/', views.delete_address, name='delete_address'),
]
