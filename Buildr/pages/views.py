from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product
def home_view(request, *args, **kwargs):
    context = {
        'all_products':Product.objects.all()
    }
    
    return render(request,"home.html",context)