"""Buildr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pages.views import home_view, products_ram_view, products_cpu_view, products_mobo_view, products_gpu_view, build_view,build_view_mobos,build_view_rams
from product.views import product_detail_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    re_path(r'^product/(ram|gpu|cpu|mobo)/(?P<id>\w+)/$', product_detail_view),
    path('products/ram',products_ram_view),
    path('build/',build_view),
    path('products/gpu',products_gpu_view),
    path('products/cpu',products_cpu_view),
    path('products/mobo',products_mobo_view),
    path('build/ajax/get/mobos',build_view_mobos),
    path('build/ajax/get/rams',build_view_rams)

]
urlpatterns+=staticfiles_urlpatterns()