from mongoengine import Document, StringField, FloatField, IntField
class Product(Document):
    # MongoEngine will automatically create an '_id' field
    name = StringField(required=True, max_length=200)
    description = StringField()
    category = StringField(max_length=100)
    price = FloatField(required=True)
    brand = StringField(max_length=100)
    quantity = IntField(required=True)

    def to_dict(self):
        """Turns the object into a dictionary so Django can send it as JSON"""
        return {
            "id": str(self.id),   # Convert ObjectId to string for JSON responses
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity
        }