import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import service

@csrf_exempt
def get_products_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    products = service.get_all_products()
    return JsonResponse([p.to_dict() for p in products], safe=False)

@csrf_exempt
def create_product_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        new_p = service.create_product(data)
        return JsonResponse(new_p.to_dict(), status=201)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def product_detail_api(request, p_id):
    product = service.get_product_by_id(p_id)
    
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(product.to_dict())

    elif request.method == "DELETE":
        service.delete_product_by_id(p_id)
        return JsonResponse({"message": "Product deleted"}, status=200)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            updated_product = service.update_product_by_id(p_id, data)
            return JsonResponse(updated_product.to_dict())
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    # Catch-all for unsupported methods on this URL
    return JsonResponse({"error": "Method not allowed"}, status=405)