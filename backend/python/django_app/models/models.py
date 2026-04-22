from datetime import datetime, timezone
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField
class ProductCategory(Document):
    
    title = StringField(required=True, unique=True, max_length=100)
    description = StringField(max_length=500)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # Set default to current time when the document is created
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc)) # Field to store the last updated timestamp

    def to_dict(self):
        """Turns the object into a dictionary so Django can send it as JSON"""
        return {
            "id": str(self.id),   # Convert ObjectId to string for JSON responses
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
class Product(Document):
    # MongoEngine will automatically create an '_id' field
    title = StringField(required=True, max_length=100)
    description = StringField()
    price = FloatField(required=True)
    brand = StringField(max_length=100, required=True)
    quantity = IntField(required=True)
    # 'reverse_delete_rule=CASCADE' means if a category is deleted, 
    # we can handle the products (usually we use NULLIFY or DENY)
    category = ReferenceField(ProductCategory, reverse_delete_rule=1)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # Set default to current time when the document is created
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc)) # Field to store the last updated timestamp

    def to_dict(self):
        """Turns the object into a dictionary so Django can send it as JSON"""
        category_title = None
        try:
            # We try to access the title. If the category doesn't exist, 
            # MongoEngine raises DoesNotExist.
            if self.category:
                category_title = self.category.title
        except:
            category_title = "Missing Category"
        return {
            "id": str(self.id),   # Convert ObjectId to string for JSON responses
            "title": self.title,
            "description": self.description,
            "category": category_title,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
