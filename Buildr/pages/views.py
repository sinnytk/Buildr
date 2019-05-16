from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product,Processor,Motherboard,Ram,Gpu,ProductPrices
from django.db.models import Max,Min
def home_view(request, *args, **kwargs):
    products=Product.objects.all()
    maxprice=Product.objects.aggregate(Max('min_price'))['min_price__max']
    minprice=Product.objects.aggregate(Min('min_price'))['min_price__min']
    if "budget" in request.GET:
        case=int(request.GET.get('sort'))
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
        if(int(request.GET.get('budget'))>0):
            products=products.filter(min_price__lte=int(request.GET.get('budget')))
        context = {
            'all_products':products
        }
        return render(request,"home_blocks/products_block.html",context)
    context = {
        'all_products': products,
        'minprice':minprice,
        'maxprice':maxprice
    }
    return render(request,"home.html",context)


def build_view(request, *args, **kwargs):
    context = {
        "cpus":Product.objects.all().filter(category="CPU").order_by("min_price"),
        "gpus":Product.objects.all().filter(category="GPU").order_by("min_price"),
        "mobos":Product.objects.all().filter(category="MOBO").order_by("min_price")
        
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
    if 'cpu' in request.GET:
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
def build_view_cpus(request, *args, **kwargs):
    if request.method == 'GET':
        mobo = Motherboard.objects.get(id=request.GET.get('mobo'))
        compatible_cpus = []
        cpus = Processor.objects.all().filter(socket=mobo.socket)
        for cpu in cpus:
            compatible_cpus.append(Product.objects.get(id=cpu.id))
    context = {
        'cpus':compatible_cpus
    }
    return render(request, "buildform/cpu_list.html",context)

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

def build_view_order(request):
    context = {}
    cpu_id = request.POST.get('cpu',0)
    ram_id = request.POST.get('ram',0)
    gpu_id = request.POST.get('gpu',0)
    mobo_id = request.POST.get('mobo',0)
    if(cpu_id != 0):
        cpu = Product.objects.get(id=cpu_id)
        cpu_prices = ProductPrices.objects.all().filter(id=cpu_id)
        context['cpu'] = cpu
        context['cpu_prices'] = cpu_prices
    if(ram_id != 0):
        ram = Product.objects.get(id=ram_id)
        ram_prices = ProductPrices.objects.all().filter(id=ram_id)
        context['ram'] = ram
        context['ram_prices'] = ram_prices
    if(gpu_id != 0):
        gpu = Product.objects.get(id=gpu_id)
        gpu_prices = ProductPrices.objects.all().filter(id=gpu_id)
        context['gpu'] = gpu
        context['gpu_prices'] = gpu_prices
    if(mobo_id != 0):
        mobo = Product.objects.get(id=mobo_id)
        mobo_prices = ProductPrices.objects.all().filter(id=mobo_id)
        context['mobo'] = mobo
        context['mobo_prices'] = mobo_prices
    return render(request, "buildform/build_order.html",context)
    
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
