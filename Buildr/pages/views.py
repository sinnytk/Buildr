from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product,Processor,Motherboard,Ram,Gpu
def home_view(request, *args, **kwargs):
    products=Product.objects.all()
    sortvalue=0
    if request.method == 'POST':
        case=int(request.POST.get('sort'))
        if(case == 1):
            sortvalue=1
            products = Product.objects.all().order_by("min_price")
        elif(case == 2):
            sortvalue=2
            products = Product.objects.all().order_by("-min_price")
        elif(case == 3):
            sortvalue=3
            products = Product.objects.all().order_by("title")
        elif(case == 4):
            sortvalue=4
            products = Product.objects.all().order_by("-title")
    context = {
        'sortvalue':sortvalue,
        'all_products': products
    }
    return render(request,"home.html",context)

def build_view(request, *args, **kwargs):
    context = {
        "cpus":Product.objects.all().filter(category="CPU").order_by("min_price"),
        "gpus":Product.objects.all().filter(category="GPU").order_by("min_price")
        
    }
    return render(request,"build.html",context)
def build_view_mobos(request, *args, **kwargs):
    if request.method == 'GET':
        cpu = Processor.objects.get(id=request.GET.get('cpu'))
        compatible_mobos = []
        mobos = Motherboard.objects.all().filter(socket=cpu.socket)
        for mobo in mobos:
            compatible_mobos.append(Product.objects.get(id=mobo.id))
    context = {
        'mobos':compatible_mobos
    }
    return render(request, "buildform/mobo_list.html",context)
def build_view_rams(request, *args, **kwargs):
    if request.method == 'GET':
        cpu = Processor.objects.get(id=request.GET.get('cpu'))
        compatible_rams = []
        if((cpu.gen>5 and cpu.brand=="INTEL") or (cpu.socket=="AM4")):
            rams = Ram.objects.all().filter(rate="DDR4")
        else:
            rams = Ram.objects.all().filter(rate="DDR3")
        for ram in rams:
            compatible_rams.append(Product.objects.get(id=ram.id))
    context = {
        'rams':compatible_rams
    }
    return render(request, "buildform/ram_list.html",context)

def products_gpu_view(request,*args,**kwargs):
    products=Product.objects.all().filter(category="GPU")
    sortvalue=0
    if request.method == 'POST':
        case=int(request.POST.get('sort'))
        if(case == 1):
            sortvalue=1
            products = Product.objects.all().filter(category="GPU").order_by("min_price")
        elif(case == 2):
            sortvalue=2
            products = Product.objects.all().filter(category="GPU").order_by("-min_price")
        elif(case == 3):
            sortvalue=3
            products = Product.objects.all().filter(category="GPU").order_by("title")
        elif(case == 4):
            sortvalue=4
            products = Product.objects.all().filter(category="GPU").order_by("-title")
    context = {
        'sortvalue':sortvalue,
        'all_products': products
    }
    return render(request,"home.html",context)
def products_ram_view(request,*args,**kwargs):
    products=Product.objects.all().filter(category="RAM")
    sortvalue=0
    if request.method == 'POST':
        case=int(request.POST.get('sort'))
        if(case == 1):
            sortvalue=1
            products = Product.objects.all().filter(category="RAM").order_by("min_price")
        elif(case == 2):
            sortvalue=2
            products = Product.objects.all().filter(category="RAM").order_by("-min_price")
        elif(case == 3):
            sortvalue=3
            products = Product.objects.all().filter(category="RAM").order_by("title")
        elif(case == 4):
            sortvalue=4
            products = Product.objects.all().filter(category="RAM").order_by("-title")
    context = {
        'sortvalue':sortvalue,
        'all_products': products
    }
    return render(request,"home.html",context)
def products_cpu_view(request,*args,**kwargs):
    products=Product.objects.all().filter(category="CPU")
    sortvalue=0
    if request.method == 'POST':
        case=int(request.POST.get('sort'))
        if(case == 1):
            sortvalue=1
            products = Product.objects.all().filter(category="CPU").order_by("min_price")
        elif(case == 2):
            sortvalue=2
            products = Product.objects.all().filter(category="CPU").order_by("-min_price")
        elif(case == 3):
            sortvalue=3
            products = Product.objects.all().filter(category="CPU").order_by("title")
        elif(case == 4):
            sortvalue=4
            products = Product.objects.all().filter(category="CPU").order_by("-title")
    context = {
        'sortvalue':sortvalue,
        'all_products': products
    }
    return render(request,"home.html",context)

def products_mobo_view(request,*args,**kwargs):
    products=Product.objects.all().filter(category="MOBO")
    sortvalue=0
    if request.method == 'POST':
        case=int(request.POST.get('sort'))
        if(case == 1):
            sortvalue=1
            products = Product.objects.all().filter(category="MOBO").order_by("min_price")
        elif(case == 2):
            sortvalue=2
            products = Product.objects.all().filter(category="MOBO").order_by("-min_price")
        elif(case == 3):
            sortvalue=3
            products = Product.objects.all().filter(category="MOBO").order_by("title")
        elif(case == 4):
            sortvalue=4
            products = Product.objects.all().filter(category="MOBO").order_by("-title")
    context = {
        'sortvalue':sortvalue,
        'all_products': products
    }
    return render(request,"home.html",context)
