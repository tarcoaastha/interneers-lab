from django.urls import path
from .views import views  # Importing views 

urlpatterns = [
    # --- PRODUCT URLS ---
    path('products/all/', views.get_products_api),
    path('products/create/', views.create_product_api),
    # Task 6: Bulk Upload
    path('products/bulk-upload/', views.bulk_upload_api),
    path('products/<str:p_id>/', views.product_detail_api),
    path('categories/remove-product/', views.remove_product_from_category_view),

    # --- CATEGORY URLS (WEEK 4) ---
    # Task 1: Create Category
    path('categories/create/', views.create_category_api),
    # Task 3: List Categories
    path('categories/list/', views.list_categories_api),
    path('categories/add-product/', views.add_product_to_category_api),
    # Task 3a: Products in Category
    path('categories/<str:category_id>/products/', views.get_products_by_category_api),
    # Task 4: Add/Remove Product from Category (If you created this view)
    # path('categories/add-product/', views.add_product_to_category_api),
]