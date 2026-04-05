import unittest
from unittest.mock import patch
from django_app.service.service import ProductCategoryService

class TestProductCategoryService(unittest.TestCase):

    @patch('django_app.service.service.ProductCategoryRepository')
    @patch('django_app.service.service.ProductRepository')
    def setUp(self, MockProductRepo, MockCategoryRepo):
        self.mock_prod_repo = MockProductRepo.return_value
        self.mock_cat_repo = MockCategoryRepo.return_value
        
        # 2. Initialize the service
        self.service = ProductCategoryService()

    #  Test create_new_category 
    def test_create_new_category_success(self):
        """Verify category is created after title is stripped."""
        data = {'title': '  Electronics  ', 'description': 'Gadgets'}
        self.mock_cat_repo.create_category.return_value = {"id": "1", "title": "Electronics"}
        
        result = self.service.create_new_category(data)
        self.assertEqual(result["title"], "Electronics")
        self.assertEqual(data['title'], "Electronics")
        self.mock_cat_repo.create_category.assert_called_once_with(data)

    def test_create_new_category_empty_title(self):
        """Verify exception is raised if title is missing."""
        with self.assertRaises(Exception) as cm:
            self.service.create_new_category({'title': ''})
        self.assertEqual(str(cm.exception), "Category title cannot be empty.")

    def test_list_all_categories(self):
        """Verify retrieval of all categories."""
        self.mock_cat_repo.get_all_categories.return_value = [{"title": "Food"}, {"title": "Toys"}]
        result = self.service.list_all_categories()
        
        self.assertEqual(len(result), 2)
        self.mock_cat_repo.get_all_categories.assert_called_once()

    def test_get_products_in_category_success(self):
        """Verify retrieval of products for a valid category."""
        self.mock_cat_repo.get_category_by_id.return_value = {"id": "cat123"}
        self.mock_prod_repo.get_products_by_category.return_value = [{"name": "Bread"}]
        
        result = self.service.get_products_in_category("cat123")
        
        self.assertEqual(len(result), 1)
        self.mock_prod_repo.get_products_by_category.assert_called_with("cat123")

    def test_get_products_in_category_not_found(self):
        """Verify exception if category ID does not exist."""
        self.mock_cat_repo.get_category_by_id.return_value = None
        
        with self.assertRaises(Exception) as cm:
            self.service.get_products_in_category("ghost_id")
        self.assertEqual(str(cm.exception), "Category not found.")

    def test_add_product_to_category_success(self):
        """Verify successful link between product and category."""
        self.mock_cat_repo.get_category_by_id.return_value = {"id": "cat_id", "title": "Home"}
        self.mock_prod_repo.get_by_id.return_value = {"id": "prod_id", "name": "Lamp"}
        self.mock_prod_repo.update.return_value = {"id": "prod_id", "category": "Home"}
        
        result = self.service.add_product_to_category("prod_id", "cat_id")
        
        self.assertEqual(result["category"], "Home")
        self.mock_prod_repo.update.assert_called_with("prod_id", {"category": {"id": "cat_id", "title": "Home"}})

    def test_add_product_to_category_product_not_found(self):
        """Verify error if product is missing during link attempt."""
        self.mock_cat_repo.get_category_by_id.return_value = {"id": "cat_id"}
        self.mock_prod_repo.get_by_id.return_value = None
        
        with self.assertRaises(Exception) as cm:
            self.service.add_product_to_category("ghost_prod", "cat_id")
        self.assertEqual(str(cm.exception), "Product not found.")

    def test_remove_product_from_category_success(self):
        """Verify category is set to None (unlinked)."""
        self.mock_prod_repo.get_by_id.return_value = {"id": "prod_id"}
        self.mock_prod_repo.update.return_value = {"id": "prod_id", "category": None}
        
        result = self.service.remove_product_from_category("prod_id")
        
        self.assertIsNone(result["category"])
        self.mock_prod_repo.update.assert_called_with("prod_id", {"category": None})

if __name__ == '__main__':
    unittest.main(verbosity=2)