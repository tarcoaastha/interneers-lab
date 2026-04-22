import json
from django.test import Client
from .base_integration import BaseIntegrationTest
from django_app.models.models import Product, ProductCategory

class TestAPIIntegration(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_create_product_api(self):
        url = '/products/create/'
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

    def test_category_and_product_flow(self):
    
        cat_url = '/categories/create/'
        cat_data = {"title": "Peripherals", "description": "PC Accessories"}
        cat_res = self.client.post(cat_url, data=json.dumps(cat_data), content_type='application/json')
        self.assertEqual(cat_res.status_code, 201)
        cat_id = cat_res.json()['id']

        product = Product(title="Keyboard", price=100, quantity=5, brand="Razer").save()

        link_url = '/categories/add-product/'
        link_data = {"product_id": str(product.id), "category_id": cat_id}
        link_res = self.client.post(link_url, data=json.dumps(link_data), content_type='application/json')
        
        self.assertEqual(link_res.status_code, 200)
        
        product.reload()
        self.assertEqual(product.category.title, "Peripherals")

    def test_bulk_upload_api(self):
        url = '/products/bulk-upload/'
        csv_content = "title,price,quantity,brand,description\nMonitor,300,2,Dell,4K Display"
        
        from io import BytesIO
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'products.csv'

        response = self.client.post(url, {'file': csv_file})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['created'], 1)

    def test_get_products_by_category_api(self):

        category, product = self.seed_data()
        
        url = f'/categories/{str(category.id)}/products/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], "Test Phone")