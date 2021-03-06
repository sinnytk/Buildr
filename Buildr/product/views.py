from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, ProductPrices, Processor, Motherboard

def product_detail_view(request, *args, **kwargs):
    obj = Product.objects.get(id=kwargs['id'])
    prices=ProductPrices.objects.all().filter(id=obj.id)
    context = {
        'object':obj,
        'prices':prices
    }

    return render(request,'product/detail.html',context)
def compatible(request, *args, **kwargs):
    if(request.GET.get('cpu') == '') or (request.GET.get('mobo') == ''):
        return JsonResponse({'notCompatible':True}) 
    cpu = Processor.objects.get(id=request.GET.get('cpu'))
    mobo = Motherboard.objects.get(id=request.GET.get('mobo'))
    same=(cpu.socket == mobo.socket)
    if same:
        return JsonResponse({'notCompatible':False})
    else:
        return JsonResponse({'notCompatible':True})
