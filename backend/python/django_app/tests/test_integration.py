from .base_integration import BaseIntegrationTest
from django_app.service.service import ProductService, ProductCategoryService

class TestProductIntegration(BaseIntegrationTest):
    def setUp(self):
        super().setUp() # Runs the database cleanup
        self.product_service = ProductService()
        self.category_service = ProductCategoryService()

    def test_create_and_retrieve_product(self):
        data = {"title": "Real Monitor", "price": 300, "quantity": 2, "brand": "Samsung"}
    
        self.product_service.create_product(data)
    
        all_products = self.product_service.get_products()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0]["title"], "Real Monitor")

    def test_add_product_to_category_integration(self):
        category, product = self.seed_data()
        updated_prod = self.category_service.add_product_to_category(
            str(product.id), str(category.id)
        )
        self.assertEqual(updated_prod.category.title, "Electronics")