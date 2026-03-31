import json
from django.test import Client
from .base_integration import BaseIntegrationTest
from django_app.models.models import Product, ProductCategory

class TestAPIIntegration(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.client = Client()

    # --- 1. Test Product Creation API ---
    def test_create_product_api(self):
        url = '/products/create/'  # Matches your path
        data = {
            "title": "Gaming Mouse",
            "price": 50.0,
            "quantity": 10,
            "brand": "Logitech",
            "description": "High DPI mouse"
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    # --- 2. Test Category Creation & Product Linking ---
    def test_category_and_product_flow(self):
        # A. Create Category
        cat_url = '/categories/create/'
        cat_data = {"title": "Peripherals", "description": "PC Accessories"}
        cat_res = self.client.post(cat_url, data=json.dumps(cat_data), content_type='application/json')
        self.assertEqual(cat_res.status_code, 201)
        cat_id = cat_res.json()['id']

        # B. Create a Product directly in DB
        product = Product(title="Keyboard", price=100, quantity=5, brand="Razer").save()

        # C. Link Product to Category via API
        link_url = '/categories/add-product/'
        link_data = {"product_id": str(product.id), "category_id": cat_id}
        link_res = self.client.post(link_url, data=json.dumps(link_data), content_type='application/json')
        
        self.assertEqual(link_res.status_code, 200)
        
        # Verify link in Database
        product.reload()
        self.assertEqual(product.category.title, "Peripherals")

    # --- 3. Test Bulk Upload API ---
    def test_bulk_upload_api(self):
        url = '/products/bulk-upload/'
        # Note: 'title' matches your new requirement
        csv_content = "title,price,quantity,brand,description\nMonitor,300,2,Dell,4K Display"
        
        from io import BytesIO
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'products.csv'

        response = self.client.post(url, {'file': csv_file})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['created'], 1)

    # --- 4. Test Fetch Products by Category ---
    def test_get_products_by_category_api(self):
        # Setup: One category with one product
        category, product = self.seed_data()
        
        url = f'/categories/{str(category.id)}/products/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], "Test Phone")