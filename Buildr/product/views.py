from django.shortcuts import render
from .models import Product, RamPrices, ProcessorPrices, MotherboardPrices, GpuPrices

def product_detail_view(request, *args, **kwargs):
    obj = Product.objects.get(id=kwargs['id'])
    if(obj.category=="RAM"):
        prices=RamPrices.objects.all().filter(id=obj.id)
    elif(obj.category=="CPU"):
        prices=ProcessorPrices.objects.all().filter(id=obj.id)
    elif(obj.category=="MOBO"):
        prices=MotherboardPrices.objects.all().filter(id=obj.id)
    elif(obj.category=="GPU"):
        prices=GpuPrices.objects.all().filter(id=obj.id)
    context = {
        'object':obj,
        'prices':prices
    }

    return render(request,'product/detail.html',context)

