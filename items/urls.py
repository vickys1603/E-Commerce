from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), # This path will be included from ecommerce_project/urls.py
    path('<int:product_id>/', views.product_detail_view, name='product_detail'),
]