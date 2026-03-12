from datetime import datetime, timezone
from mongoengine import NotUniqueError, ValidationError
from ..models.models import Product, ProductCategory
class ProductRepository:
    """
    Handles all direct MongoDB operations for the Product collection."""
    
    def create(self, data):
        """Creates a new product in the database"""
        product = Product(**data)
        product.save()
        return product
    
    def get_all(self):
        """Retrieves all products from the database"""
        return Product.objects().all().order_by('-created_at')  # Sort by creation time, newest first
    
    def get_by_id(self, product_id):
        """Retrieves a product by its ID"""
        return Product.objects(id=product_id).first()
    
    def update(self, product_id, data):
        """Updates a product's details"""
        product = self.get_by_id(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        product.updated_at = datetime.now(timezone.utc)  # Update the timestamp when the product is updated
        product.save()
        return product
    
    def delete(self, product_id):
        """Deletes a product from the database"""
        product = self.get_by_id(product_id)
        if not product:
            return False
        product.delete()
        return True
    def get_products_by_category(self, category_id):
        """Task 3a: Fetches products filtered by a specific category ID"""
        return Product.objects(category=category_id)
    
class ProductCategoryRepository:
    
    def create_category(self, data):
        """Task 1: Creates a new category like 'Food'"""
        try:
            category = ProductCategory(
                title=data.get('title'),
                description=data.get('description')
            )
            category.save()
            return category
        except NotUniqueError:
            raise Exception("A category with this title already exists.")
        except ValidationError as e:
            raise Exception(f"Validation Error: {str(e)}")

    def get_all_categories(self):
        """Task 3: Fetches all categories for the list view"""
        return ProductCategory.objects().order_by('title')

    def get_category_by_id(self, category_id):
        """Helper to find a category before adding/removing products"""
        return ProductCategory.objects(id=category_id).first()