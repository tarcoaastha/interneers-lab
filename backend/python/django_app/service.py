from .models import Product

# This is our IN-MEMORY database. 
# It is just a simple Python list.
products_storage = []
next_id = 1
def create_product_service(data):
    global next_id
    
    # --- VALIDATION LOGIC ---
    name = data.get('name', '').strip()
    price = data.get('price')
    quantity = data.get('quantity')

    # Rule 1: Name cannot be empty
    if not name:
        raise ValueError("Product name is required.")
    
    # Rule 2: Price must be a positive number
    try:
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
    except (TypeError, ValueError):
        raise ValueError("Invalid price format.")

    # Rule 3: Quantity cannot be negative
    if int(quantity) < 0:
        raise ValueError("Quantity cannot be negative.")
    

    new_product = Product(
        id=next_id,
        name=name,
        description=data.get('description'),
        category=data.get('category'),
        price=price,
        brand=data.get('brand'),
        quantity=int(quantity)
    )
    
    products_storage.append(new_product)
    next_id += 1
    return new_product
def get_all_products_service():
    return products_storage
def get_product_by_id_service(p_id):
    for product in products_storage:
        if product.id == p_id:
            return product   
    return None
def delete_product_by_id_service(p_id):
    global products_storage
    products_storage = [product for product in products_storage if product.id != p_id]
def update_product_by_id_service(p_id, data):
    for product in products_storage:
        if product.id == p_id:
            product.name = data.get("name", product.name)
            product.description = data.get("description", product.description)
            product.category = data.get("category", product.category)
            product.price = data.get("price", product.price)
            product.brand = data.get("brand", product.brand)
            product.quantity = data.get("quantity", product.quantity)
            return product
    return None