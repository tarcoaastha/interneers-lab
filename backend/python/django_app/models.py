class Product:
    def __init__(self, id, name, description, category, price, brand, quantity):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.brand = brand
        self.quantity = quantity

    def to_dict(self):
        """Turns the object into a dictionary so Django can send it as JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity
        }