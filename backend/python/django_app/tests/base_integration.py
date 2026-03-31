import unittest
from mongoengine import connect, disconnect
from django_app.models.models import Product, ProductCategory

class BaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Connect to a LOCAL test database (making sure MongoDB is running and accessible)
        disconnect(alias='default')
        db_uri = "mongodb://root:example@127.0.0.1:27017/product_db?authSource=admin"
        cls.db = connect('test_db', host=db_uri)

    @classmethod
    def tearDownClass(cls):
        # 2. Disconnect when all tests are finished
        disconnect(alias='default')

    def setUp(self):
        # 3. Clean the database before EVERY test to avoid data leaking
        Product.objects.delete()
        ProductCategory.objects.delete()

    def seed_data(self):
        """Helper method to seed basic data for tests"""
        category = ProductCategory(title="Electronics", description="Gadgets").save()
        product = Product(
            title="Test Phone", 
            price=500, 
            quantity=10, 
            brand="Apple", 
            category=category
        ).save()
        return category, product