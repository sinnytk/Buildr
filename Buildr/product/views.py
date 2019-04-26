from django.shortcuts import render
from .models import Product

def product_detail_view(request, *args, **kwargs):
    obj = Product.objects.get(id='ZTT20810D10P')
    context = {
        'object':obj
    }
    return render(request,'product/detail.html',context)

