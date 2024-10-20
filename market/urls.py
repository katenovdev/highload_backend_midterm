from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserCreateView.as_view(), name='user-register'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('category/create', CategoryListCreateView.as_view(), name='category-list-create'),
    path('product/create', ProductListCreateView.as_view(), name='product-list-create'),
    path('category/get-list', CategoryListView.as_view(), name='category-list'),  
    path('products/get-list', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  
    path('order/create', OrderCreateView.as_view(), name='order-create'),
]
