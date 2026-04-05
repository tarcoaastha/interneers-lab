# import unittest
# from unittest.mock import MagicMock, patch
# from django_app.service.service import ProductService
#commented out old unittest code in favor of pytest style tests with fixtures and parameterization
# class TestProductService(unittest.TestCase):

#     @patch('django_app.service.service.ProductRepository')
#     def setUp(self, MockRepoClass):
#         # Created a mock instance of the repository
#         self.mock_repo = MockRepoClass.return_value
#         self.service = ProductService()

#     # --- 1. Test validate_product_data ---
#     def test_validate_product_data_missing_field(self):
#         """Test that missing required fields raise ValueError."""
#         data = {"title": "Laptop", "price": 100} # Missing quantity and brand
#         with self.assertRaises(ValueError) as cm:
#             self.service.validate_product_data(data, is_update=False)
#         self.assertIn("required", str(cm.exception))

#     def test_validate_product_data_invalid_price(self):
#         """Test that non-positive price raises ValueError."""
#         data = {"title": "Laptop", "price": 0, "quantity": 1, "brand": "Dell"}
#         with self.assertRaises(ValueError) as cm:
#             self.service.validate_product_data(data)
#         self.assertEqual(str(cm.exception), "Price must be a positive number.")

#     # --- 2. Test create_product ---
#     def test_create_product_success(self):
#         """Test successful product creation."""
#         data = {"title": "Laptop", "price": 1000, "quantity": 5, "brand": "Dell"}
#         self.mock_repo.create.return_value = {"id": "123", **data}
        
#         result = self.service.create_product(data)
        
#         self.assertEqual(result["id"], "123")
#         self.mock_repo.create.assert_called_once_with(data)

#     # --- 3. Test get_products ---
#     def test_get_products_mapping(self):
#         """Test retrieval and to_dict mapping."""
#         # Create a mock product that has a to_dict method
#         mock_p = MagicMock()
#         mock_p.to_dict.return_value = {"title": "Mouse"}
        
#         self.mock_repo.get_all.return_value.order_by.return_value = [mock_p]
        
#         result = self.service.get_products()
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]["title"], "Mouse")

#     # --- 4. Test delete_product_by_id ---
#     def test_delete_product_by_id(self):
#         """Test that delete is called correctly."""
#         self.mock_repo.delete.return_value = True
#         result = self.service.delete_product_by_id("123")
#         self.assertTrue(result)
#         self.mock_repo.delete.assert_called_with("123")

#     # --- 5. Test update_product_by_id ---
#     def test_update_product_success(self):
#         """Test successful update with validation."""
#         update_data = {"price": 500}
#         self.mock_repo.update.return_value = {"id": "123", "price": 500}
        
#         result = self.service.update_product_by_id("123", update_data)
#         self.assertEqual(result["price"], 500)
#         self.mock_repo.update.assert_called_with("123", update_data)

#     def test_update_product_not_found(self):
#         """Test error when product to update doesn't exist."""
#         self.mock_repo.update.return_value = None
#         with self.assertRaises(Exception) as cm:
#             self.service.update_product_by_id("999", {"title": "Ghost"})
#         self.assertIn("not found", str(cm.exception))

#     # --- 6. Test get_product_by_id ---
#     def test_get_product_by_id(self):
#         """Test getting a single product."""
#         self.mock_repo.get_by_id.return_value = {"title": "Tablet"}
#         result = self.service.get_product_by_id("123")
#         self.assertEqual(result["title"], "Tablet")

#     # --- 7. Test bulk_upload_products_from_csv ---
#     def test_bulk_upload_success(self):
#         """Test CSV parsing and creation logic."""
#         csv_content = "title,price,quantity,brand,description\nPhone,500,10,Apple,Nice Phone"
#         # Mock the file object
#         mock_file = MagicMock()
#         mock_file.read.return_value = csv_content.encode('utf-8')
        
#         # Mock create_product to succeed
#         with patch.object(self.service, 'create_product') as mock_create:
#             result = self.service.bulk_upload_products_from_csv(mock_file)
            
#             self.assertEqual(result["created"], 1)
#             self.assertEqual(len(result["errors"]), 0)
#             mock_create.assert_called_once()




# if __name__ == '__main__':
#     unittest.main(verbosity=2)


import pytest
import io
from unittest.mock import MagicMock, patch
from django_app.service.service import ProductService

# We use a class to keep things organized, but no longer need unittest.TestCase
class TestProductService:

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        """This replaces the old setUp method using patches."""
        with patch('django_app.service.service.ProductRepository') as MockRepoClass:
            self.mock_repo = MockRepoClass.return_value
            self.service = ProductService()
            yield # This allows the tests to run

    # --- 1. Parameterized Validation Tests ---
    @pytest.mark.parametrize("test_input, expected_error_msg", [
        # Scenario 1: Missing quantity and brand
        ({"title": "Laptop", "price": 100}, "Product quantity is required."),
        
        # Scenario 2: Invalid Price
        ({"title": "Laptop", "price": 0, "quantity": 1, "brand": "Dell"}, "Price must be a positive number."),
        
        # Scenario 3: Negative Quantity
        ({"title": "Laptop", "price": 100, "quantity": -5, "brand": "Dell"}, "Quantity cannot be negative."),
        
        # Scenario 4: Empty Title
        ({"title": "  ", "price": 100, "quantity": 1, "brand": "Dell"}, "Field 'title' cannot be empty or just spaces."),
    ])
    def test_validate_product_data_scenarios(self, test_input, expected_error_msg):
        """Tests multiple validation failures in one function."""
        with pytest.raises(ValueError) as excinfo:
            self.service.validate_product_data(test_input)
        assert expected_error_msg in str(excinfo.value)

    # --- 2. Success Test (Happy Path) ---
    def test_create_product_success(self):
        data = {"title": "Laptop", "price": 1000, "quantity": 5, "brand": "Dell"}
        self.mock_repo.create.return_value = {"id": "123", **data}
        
        result = self.service.create_product(data)
        
        assert result["id"] == "123"
        self.mock_repo.create.assert_called_once_with(data)

    # --- 3. Parameterized Get/Update/Delete ---
    @pytest.mark.parametrize("method_name, arg, repo_return, expected", [
        ("delete_product_by_id", "123", True, True),
        ("get_product_by_id", "123", {"title": "Tablet"}, {"title": "Tablet"}),
    ])
    def test_basic_repo_calls(self, method_name, arg, repo_return, expected):
        """Tests simple repository delegation."""
        # Dynamically get the method and the mock repo method
        service_method = getattr(self.service, method_name)
        repo_method = getattr(self.mock_repo, "delete" if "delete" in method_name else "get_by_id")
        
        repo_method.return_value = repo_return
        result = service_method(arg)
        
        assert result == expected

    # --- 4. Bulk Upload Test ---
    def test_bulk_upload_success(self):
        csv_content = "title,price,quantity,brand,description\nPhone,500,10,Apple,Nice Phone"
        mock_file = MagicMock()
        mock_file.read.return_value = csv_content.encode('utf-8')
        
        with patch.object(self.service, 'create_product') as mock_create:
            result = self.service.bulk_upload_products_from_csv(mock_file)
            assert result["created"] == 1
            mock_create.assert_called_once()