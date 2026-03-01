import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import service

@csrf_exempt
def product_list_api(request):
    """Handles multiple products: GET (List) and POST (Create)"""
    
    if request.method == "GET":
        # Get the list of objects from the service
        products = service.get_all_products_service()
        # Convert objects to dictionaries so we can send them as JSON
        output = [p.to_dict() for p in products]
        return JsonResponse(output, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_p = service.create_product_service(data)
            return JsonResponse(new_p.to_dict(), status=201)
        except ValueError as e:
            # Send back the specific error message with a 400 Bad Request code
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def product_detail_api(request, p_id):
    """Handles a single product: GET (Fetch), PUT (Update), DELETE (Remove)"""
    
    product = service.get_product_by_id_service(p_id)
    
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(product.to_dict())

    if request.method == "DELETE":
        service.delete_product_by_id_service(p_id)
        return JsonResponse({"message": "Product deleted"}, status=200)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        updated_product = service.update_product_by_id_service(p_id, data)
        if updated_product:
            return JsonResponse(updated_product.to_dict())
        else:
            return JsonResponse({"error": "Product not found"}, status=404)