from .models import Product
class ProductRepository:
    """
    Handles all direct MongoDB operations for the Product collection."""
    @staticmethod
    def create(data):
        """Creates a new product in the database"""
        product = Product(**data)
        product.save()
        return product
    @staticmethod
    def get_all():
        """Retrieves all products from the database"""
        return Product.objects().all()
    @staticmethod
    def get_by_id(product_id):
        """Retrieves a product by its ID"""
        return Product.objects(id=product_id).first()
    @staticmethod
    def update(product_id, data):
        """Updates a product's details"""
        product = Product.objects(id=product_id).first()
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product
    @staticmethod
    def delete(product_id):
        """Deletes a product from the database"""
        product = Product.objects(id=product_id).first()
        if not product:
            return False
        product.delete()
        return True