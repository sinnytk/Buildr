from django.shortcuts import render
from django.http import HttpResponse
def home_view(request, *args, **kwargs):
    print(request.path)
    return render(request,"home.html",{})