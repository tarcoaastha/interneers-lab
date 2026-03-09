from datetime import datetime, timezone
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
class Product(Document):
    # MongoEngine will automatically create an '_id' field
    name = StringField(required=True, max_length=200)
    description = StringField()
    category = StringField(max_length=100)
    price = FloatField(required=True)
    brand = StringField(max_length=100)
    quantity = IntField(required=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # Set default to current time when the document is created
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc)) # Field to store the last updated timestamp

    def to_dict(self):
        """Turns the object into a dictionary so Django can send it as JSON"""
        return {
            "id": str(self.id),   # Convert ObjectId to string for JSON responses
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }