
from django.contrib import admin
from django.urls import path
from scraper_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.display_product_list, name='home'),

]