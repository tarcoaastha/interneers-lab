from .models import Product

# IN-MEMORY database
products_storage = []

def validate_product_data(data):
    """Common validation logic shared by Create and Update"""
    name = data.get('name', '').strip()
    price = data.get('price')
    quantity = data.get('quantity')

    if not name:
        raise ValueError("Product name is required.")
    
    try:
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
    except (TypeError, ValueError):
        raise ValueError("Invalid price format.")

    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
    except (TypeError, ValueError):
        raise ValueError("Invalid quantity format.")   
    
    return name, price, quantity

def create_product(data):
    name, price, quantity = validate_product_data(data)
    new_id = len(products_storage) + 1

    new_product = Product(
        id=new_id,
        name=name,
        description=data.get('description'),
        category=data.get('category'),
        price=price,
        brand=data.get('brand'),
        quantity=quantity
    )
    
    products_storage.append(new_product)
    return new_product

def get_all_products():
    return products_storage

def get_product_by_id(p_id):
    for product in products_storage:
        if product.id == p_id:
            return product   
    return None

def delete_product_by_id(p_id):
    global products_storage
    initial_len = len(products_storage)
    products_storage = [p for p in products_storage if p.id != p_id]
    return len(products_storage) < initial_len

def update_product_by_id(p_id, data):
    product = get_product_by_id(p_id)
    if not product:
        return None
    
    name, price, quantity = validate_product_data(data)
    
    product.name = name
    product.price = price
    product.quantity = quantity
    product.description = data.get('description', product.description)
    product.brand = data.get('brand', product.brand)
    product.category = data.get('category', product.category)
    
    for i, p in enumerate(products_storage):
        if p.id == p_id:
            products_storage[i] = product
            break      
    return product