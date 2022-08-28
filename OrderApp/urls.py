from django.urls import path
from OrderApp.views import Add_to_Shopping_cart, cart_details, cart_delete, order_cart, order_showing, order_product_showing, user_order_details, user_order_product_details

urlpatterns = [
    path('addingcart/<int:id>', Add_to_Shopping_cart, name='Add_to_Shopping_cart'),
    path('cart_details/', cart_details, name='cart_details'),
    path('cart_delete/<int:id>', cart_delete, name = 'cart_delete'),
    path('order_cart/', order_cart, name='order_cart'),
    path('order_list/', order_showing, name='order_list'),
    path('order_product_showing/', order_product_showing, name='order_product_showing'),
    path('order_details/<int:id>', user_order_details, name='user_order_details'),
    path('order_product_details/<int:id>/<int:oid>/', user_order_product_details, name='user_order_product_details'),
]