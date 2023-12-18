from django.urls import path
from scraper_app import views

urlpatterns = [
    path('', views.display_product_list, name='product_list'),  # Update this line
    # Other URL patterns...
]
