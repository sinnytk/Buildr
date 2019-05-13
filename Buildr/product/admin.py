from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Processor)
admin.site.register(Motherboard)
admin.site.register(Gpu)
admin.site.register(Ram)
admin.site.register(ProductPrices)