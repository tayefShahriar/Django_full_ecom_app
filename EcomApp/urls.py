from django.urls import path
from .views import Home, product_single, category_product, about, contact, SearchView

urlpatterns = [
    path("", Home, name = 'Home'),
    path("product/<int:id>/", product_single, name = 'product_single'),
    path("product/<int:id>/<slug:slug>/", category_product, name = 'category_product'),
    path("about/", about, name = 'about'),
    path("contact/", contact, name = 'contact_dat'),
    path('search/', SearchView, name='SearchView'),
]