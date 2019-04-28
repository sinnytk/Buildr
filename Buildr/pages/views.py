from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product
def home_view(request, *args, **kwargs):
    context = {
        'all_products':Product.objects.all()
    }
    return render(request,"home.html",context)

def products_gpu_view(request,*args,**kwargs):
    context = {
    'all_products':Product.objects.filter(category="GPU").all()
    }
    return render(request,"home.html",context)
def products_ram_view(request,*args,**kwargs):
    context = {
    'all_products':Product.objects.filter(category="RAM").all()
    }
    return render(request,"home.html",context)
def products_cpu_view(request,*args,**kwargs):
    context = {
    'all_products':Product.objects.filter(category="CPU").all()
    }
    return render(request,"home.html",context)

def products_mobo_view(request,*args,**kwargs):
    context = {
    'all_products':Product.objects.filter(category="MOBO").all()
    }
    return render(request,"home.html",context)
