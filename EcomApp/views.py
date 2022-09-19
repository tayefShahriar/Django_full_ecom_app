from django.shortcuts import render, HttpResponseRedirect, reverse
from EcomApp.models import Setting, ContactMessage, ContactForm, FAQ
from product.models import Product, Images, Category, Comment, Color, Size, Variants
from EcomApp.forms import SearchForm
from OrderApp.models import ShopCart
# Create your views here.
def Home(request):
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    quant = 0
    for p in cart_product:
        total_amount += p.product.new_price * p.quantity
        quant += p.quantity

    sliding_images = Product.objects.all().order_by('id')[:3]
    latest_products = Product.objects.all().order_by('-id')
    products = Product.objects.all()


    context = {

        'sliding_images': sliding_images,
        'latest_products': latest_products,
        'products': products,
        'cart_product': cart_product,
        'total_amount': total_amount,
        'quant': quant,
    }
    return render(request, 'mainbody.html', context)

def about(request):
    context = {
    }
    return render(request, 'about.html', context)

def product_single(request, id):
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id = id)
    products = Product.objects.all().order_by('id')[:4]
    comment_show = Comment.objects.filter(product_id=id, status=True)
    context = {
        'single_product': single_product,
        'images': images,
        'products': products,
        'comment_show': comment_show,
    }
    if product.variant != "None":
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size-id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'query': query,
        })

    return render(request, 'product_single.html', context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action' == 'post'):
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'render_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def category_product(request, id, slug):
    sliding_images = Product.objects.all().order_by('id')[:3]
    product_cat = Product.objects.filter(category_id = id)
    context = {
        'product_cat': product_cat,
        'sliding_images': sliding_images,
    }
    return render(request, 'category_products.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #messages.success(request, 'Your message has been sent.')
            return HttpResponseRedirect(reverse('contact_dat'))

    form = ContactForm
    context = {
        'form': form,
    }
    return render(request, 'contact_form.html', context)

def SearchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cat_id = form.cleaned_data['cat_id']
            if cat_id == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=cat_id)
            sliding_images = Product.objects.all().order_by('id')[:2]
            context = {
                'query': query,
                'product_cat': products,
                'sliding_images': sliding_images,
            }
            return render(request, 'category_products.html', context)
        return HttpResponseRedirect('category_product')

def faq_details(request):
    faq = FAQ.objects.filter(status=True).order_by('created_at')
    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)