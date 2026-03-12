import sys
import os
from mongoengine import connect

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.python.django_app.models.models import Product

print("Connecting...")
connect(
    db='product_db',
    host='127.0.0.1',
    port=27017,
    username='root',
    password='example',
    authentication_source='admin'
)


print(f"Connected! DB Names: {Product._get_db().list_collection_names()}")

def migrate_existing_products_add_brand():
    print("Starting Brand Migration...")
    
    # Find products that don't have the 'brand' field
    old_products = Product.objects(brand__exists=False)
    
    # We use a list to avoid cursor timeout issues during the update
    products_to_fix = list(old_products)
    print(f"Found {len(products_to_fix)} products missing a brand.")

    count = 0
    for product in products_to_fix:
        product.brand = "Generic"
        product.save()
        count += 1
        print(f"Updated: {product.name}")
        
    print(f"Finished! Successfully updated {count} products.")

if __name__ == "__main__":
    migrate_existing_products_add_brand()