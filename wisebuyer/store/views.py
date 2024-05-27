from django.shortcuts import render
from .models import Product

def update_user(request):
    return render(request, 'update_user.html', {})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})