from django.urls import path
from . import views  # Importing views 

urlpatterns = [

    path('products/all/', views.get_products_api),
    path('products/create/', views.create_product_api),
    

    path('products/<int:p_id>/', views.product_detail_api),
]