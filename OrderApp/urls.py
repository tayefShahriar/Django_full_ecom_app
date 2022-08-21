from django.urls import path
from OrderApp.views import Add_to_Shopping_cart, cart_details, cart_delete

urlpatterns = [
    path('addingcart/<int:id>', Add_to_Shopping_cart, name='Add_to_Shopping_cart'),
    path('cart_details/', cart_details, name='cart_details'),
    path('cart_delete/<int:id>', cart_delete, name = 'cart_delete'),
]