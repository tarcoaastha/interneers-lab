from .repository import ProductRepository
def validate_product_data(data, is_update=False):
    """
    Helper function to validate product input.
    If is_update is True, we might allow missing fields.
    """    
    # For a new product, name, price, and quantity are mandatory
    
    if not is_update:
        for field in ["name", "price", "quantity"]:
            if field not in data:
                raise ValueError(f"Product {field} is required.")# Common validations for both create and update
   # 2. Universal Logic (Checks any field that IS in the data)
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
def create_product(data):
    validate_product_data(data)
    return ProductRepository.create(data)
def get_all_products():
    return ProductRepository.get_all()
def delete_product_by_id(p_id):
    return ProductRepository.delete(p_id)
def update_product_by_id(p_id, data):
    validate_product_data(data, is_update=True)
    return ProductRepository.update(p_id, data)
def get_product_by_id(p_id):
    return ProductRepository.get_by_id(p_id)