import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .service import ProductService, ProductCategoryService 

# Initialize our services
product_service = ProductService()
category_service = ProductCategoryService()

@csrf_exempt
def bulk_upload_api(request):
    """Task 6: API endpoint for CSV upload"""
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)
        
        csv_file = request.FILES['file']
        
        # Check if it's actually a CSV
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File must be a CSV"}, status=400)

        result = product_service.bulk_upload_products_from_csv(csv_file)
        return JsonResponse(result)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def get_products_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    products = product_service.get_all_products()
    return JsonResponse([p.to_dict() for p in products], safe=False)

@csrf_exempt
def create_product_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        new_p = product_service.create_product(data)
        return JsonResponse(new_p.to_dict(), status=201)
    except Exception as e: # Catching general exceptions from service
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def product_detail_api(request, p_id):
    product = product_service.get_product_by_id(p_id)
    
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(product.to_dict())

    elif request.method == "DELETE":
        product_service.delete_product_by_id(p_id)
        return JsonResponse({"message": "Product deleted"}, status=200)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            updated_product = product_service.update_product_by_id(p_id, data)
            return JsonResponse(updated_product.to_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt # Added this so POST requests work!
def create_category_api(request):
    """Task 1: POST api to create a new category"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_category = category_service.create_new_category(data)
            return JsonResponse(new_category.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def add_product_to_category_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        p_id = data.get("product_id")
        c_id = data.get("category_id")
        
        # Use your category_service (ProductCategoryService)
        category_service.add_product_to_category(p_id, c_id)
        return JsonResponse({"message": "Product linked to category successfully!"})

def list_categories_api(request):
    """Task 3: GET api to fetch all categories"""
    if request.method == "GET":
        categories = category_service.list_all_categories()
        data = [cat.to_dict() for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def get_products_by_category_api(request, category_id):
    """Task 3a: GET api to fetch products belonging to a category"""
    if request.method == "GET":
        try:
            products = category_service.get_products_in_category(category_id)
            data = [prod.to_dict() for prod in products]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)
