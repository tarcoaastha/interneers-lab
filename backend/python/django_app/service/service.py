from turtle import title

from ..repositories.repository import ProductRepository, ProductCategoryRepository
import csv
import io
class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()
    def validate_product_data(self, data, is_update=False):
        """
        Helper function to validate product input.
        If is_update is True, we might allow missing fields.
        """    
        required_fields = ["name", "price", "quantity", "brand"]
        # For a new product, name, price, and quantity are mandatory
    
        if not is_update:
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Product {field} is required.")# Common validations for both create and update
        # Checks any field that IS in the data
        for field, value in data.items():
            # Check A: Block Nulls or Spaces for strings
            if isinstance(value, str):
                if not value.strip():
                    raise ValueError(f"Field '{field}' cannot be empty or just spaces.")
            
            # Check B: Block Nulls for numbers
            if value is None:
                raise ValueError(f"Field '{field}' cannot be null.")
            
        if data.get("price") is not None and data["price"] <= 0:
            raise ValueError("Price must be a positive number.")

        if data.get("quantity") is not None and data["quantity"] < 0:
            raise ValueError("Quantity cannot be negative.")
        
    def create_product(self,data):
        self.validate_product_data(data)
        return self.product_repo.create(data)
    
    def get_products(self, title=None, sort_by=None, min_price=None, max_price=None):
        query = self.product_repo.get_all()
        if title and title.strip():
            query = query.filter(title__exists=True, title__ne=None, title__icontains=title)
        if min_price:
            query = query.filter(price__gte=float(min_price))
        if max_price:
            query = query.filter(price__lte=float(max_price))
        if sort_by == "price_low":
            query = query.order_by('price')
        elif sort_by == "price_high":
            query = query.order_by('-price')
        else:
            query = query.order_by('-created_at')
        return [p.to_dict() for p in query]
    
    def delete_product_by_id(self, p_id):
        return self.product_repo.delete(p_id)
    
    def update_product_by_id(self,p_id, data):
        try:    
            self.validate_product_data(data, is_update=True)
            updated_product = self.product_repo.update(p_id, data)
            if not updated_product:
                raise ValueError(f"Product with ID {p_id} not found.")
            return updated_product
        except Exception as e:
            raise Exception(f"Error updating product: {str(e)}")
    def get_product_by_id(self, p_id):
        return self.product_repo.get_by_id(p_id)
    
    def bulk_upload_products_from_csv(self, csv_file):
        """Task 6: Bulk POST api which accepts a CSV and creates products"""
        
        # 1. Read the file
        # We use io.StringIO to turn the uploaded 'bytes' into a text stream
        file_data = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file_data))
        
        created_count = 0
        errors = []

                # 2. Loop through each row in the CSV
        for row in reader:
            try:
                # Clean the row keys in case there are hidden spaces
                clean_row = {k.strip(): v for k, v in row.items() if k}
                
                product_data = {
                    "name": clean_row.get("name"),
                    "price": float(clean_row.get("price", 0)),
                    "quantity": int(clean_row.get("quantity", 0)),
                    "brand": clean_row.get("brand"),
                    "description": clean_row.get("description", "")
                }
                
                self.create_product(product_data)
                created_count += 1              
            except Exception as e:
                # If one row fails, we keep track of the error but keep going
                errors.append(f"Row {created_count + len(errors) + 1}: {str(e)}")

        return {
            "status": "success",
            "created": created_count,
            "errors": errors
        }

class ProductCategoryService:
    def __init__(self):
        self.category_repo = ProductCategoryRepository()
        self.product_repo = ProductRepository()

    def create_new_category(self, data):
        """Task 1: Business logic for creating a category"""
        if not data.get('title'):
            raise Exception("Category title cannot be empty.")
        if 'title' in data:
            data['title'] = data['title'].strip()  
        return self.category_repo.create_category(data)
    
    def list_all_categories(self):
        """Task 3: Logic for fetching the list of all categories"""
        return self.category_repo.get_all_categories()

    def get_products_in_category(self, category_id):
        """Task 3a: Logic for fetching products belonging to a specific category"""
        # First, we check if the category actually exists
        category = self.category_repo.get_category_by_id(category_id)
        if not category:
            raise Exception("Category not found.")
            
        # Then, we ask the Product Repository for items linked to this ID
        return self.product_repo.get_products_by_category(category_id)
    
    def add_product_to_category(self, product_id, category_id):
        """Task 4: Links a product to a specific category"""
        # Verify the category exists
        category = self.category_repo.get_category_by_id(category_id)
        if not category:
            raise Exception("Category not found.")
        # Verify the product exists
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise Exception("Product not found.")
        # Update the product's category field and save
        # using the product_repo's update method
        updated_product = self.product_repo.update(product_id, {"category": category})
        return updated_product

    def remove_product_from_category(self, product_id):
        """Task 4: Removes the link between a product and its category"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise Exception("Product not found.")
        # Set category to None to break the link
        updated_product = self.product_repo.update(product_id, {"category": None})
        return updated_product