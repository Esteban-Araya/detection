from django.shortcuts import render
from detector.detec.use import ReconocedorFacial
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.
reconocedor = ReconocedorFacial()

@csrf_exempt
def imag(request):
    #print(request.body)
    a = reconocedor.image_detected(request.body)
    
    return JsonResponse({"a": a})