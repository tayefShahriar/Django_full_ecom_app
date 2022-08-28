from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from OrderApp.models import ShopCart, ShoppingCartForm, Order, OrderForm, OrderProduct
from product.models import Category, Product, Images
from EcomApp.models import Setting
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from UserApp.views import UserProfile
# Create your views here.

def Add_to_Shopping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
    if checking:
        control = 1
    else:
        control = 0

    if request.method == "POST":
        form = ShoppingCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            messages.success(request, "Your product has been added successfully!")
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Your product has been added successfully!")
        return HttpResponseRedirect(url)

def cart_details(request):
    current_user = request.user
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price * p.quantity
    context = {
        'category': category,
        'setting': setting,
        'cart_product': cart_product,
        'total_amount': total_amount,
    }
    return render(request, 'cart_details.html', context)

def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id, id=id)
    cart_product.delete()
    messages.warning(request, "Your product has been deleted!")
    return HttpResponseRedirect(url)

@login_required(login_url='/user/login')
def order_cart(request):
    current_user = request.user
    shopping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shopping_cart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            dat.code = ordercode
            dat.save()

            for rs in shopping_cart:
                data = OrderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()

            messages.success(request, "Your order has been completed")
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            context = {
                'ordercode': ordercode,
                'category': category,
                'setting': setting,
            }
            return render(request, 'order_completed.html', context)
        else:
            messages.warning(request, form.errors)

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shopping_cart:
        total_amount += p.product.new_price * p.quantity
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    context = {
        'shopping_cart': shopping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'category': category,
        'setting': setting,
        'total_amount': total_amount,
    }
    return render(request, 'order_form.html', context)

def order_showing(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    orders = Order.objects.filter(user_id = current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'orders': orders,
    }
    return render(request, 'user_order_showing.html', context)

def order_product_showing(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id = current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'order_product': order_product,
    }
    return render(request, 'order_product_list.html', context)

@login_required(login_url="/users/login")
def user_order_details(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_products = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'category': category,
        'setting': setting,
        'order_products': order_products,
    }
    return render(request, 'user_order_details.html', context)

@login_required(login_url="/users/login")
def user_order_product_details(request, id, oid):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    order_products = OrderProduct.objects.get(user_id=current_user.id, id=id)
    context = {
        'order': order,
        'category': category,
        'setting': setting,
        'order_products': order_products,
    }
    return render(request, 'user_order_product_details.html', context)

