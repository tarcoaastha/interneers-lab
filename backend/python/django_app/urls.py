from django.urls import path
from .views import product_list_api, product_detail_api

urlpatterns = [
    # For /products/
    path('products/', product_list_api),
    
    # For /products/1/, /products/2/, etc.
    path('products/<int:p_id>/', product_detail_api),
]