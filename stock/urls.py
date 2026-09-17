from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('categories/', views.category_list, name='home'),
    path('create_category/', views.category_create, name='create_category'),
    path('category_detail/<int:pk>/', views.category_detail, name='category_detail'),
    path('category_update/<int:pk>/', views.category_update, name='category_update'),
    path('delete_category/<int:pk>/', views.category_delete, name='delete_category'),

    path('product_list/', views.product_list, name='product_list'),
    path('create_product/', views.product_create, name='create_product'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('product_update/<int:pk>/', views.product_update, name='product_update'),
    path('delete_product/<int:pk>/', views.product_delete, name='delete_product'),

    path('add_stock_movement/<int:pk>/', views.add_stock_movement, name='add_stock_movement'),
]