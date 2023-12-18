# views.py in scraper_app

from django.shortcuts import render
from .models import Product

def display_product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
