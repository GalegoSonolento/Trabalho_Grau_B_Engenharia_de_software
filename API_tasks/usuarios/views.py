from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

def lista_usuarios(request):
    usuarios = [
        {'id': 1, 'name': 'João'},
        {'id': 2, 'name': 'Pedro'},
    ]
    return JsonResponse({'usuarios': usuarios})

@api_view(['GET'])
def secure_data(request):
    return Response({"message": "This is secure data"})