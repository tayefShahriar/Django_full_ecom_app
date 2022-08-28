from django.urls import path
from product.views import comment_add
urlpatterns = [
    path('comment_add/<int:id>', comment_add, name='comment_add'),
]