from django.shortcuts import render
from detector.detec.useReconocedorFacial import ReconocedorFacial
from detector.detec.detect_arrow import devolver_flecha
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.
reconocedor = ReconocedorFacial()

@csrf_exempt
def face_detect(request):
    #print(request.body)
    a = reconocedor.recoconcedor_caras(request.body)
    
    return JsonResponse({"a": a})


@csrf_exempt
def flecha(request):

    direction = devolver_flecha(request.body)

    return JsonResponse({"direction": direction})