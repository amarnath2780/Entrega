from atexit import register
from multiprocessing import context
from django.shortcuts import render , get_object_or_404 ,redirect
from advertisemennt.models import Logo
from cart.views import _cart_id
from cart.models import CartItem
from store.forms import ReviewForms
from .models import Products, ReviewRating
from category.models import Category
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
from django.contrib import messages

# Create your views here.


def submit_review(request , product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        print('POST')
        try:
            review = ReviewRating.objects.get(user__id = request.user.id , product__id = product_id)
            form = ReviewForms(request.POST  ,  instance=review)
            form.save()
             
            messages.success(request , 'Thank you Your review has been Updated . ')

            return redirect(product_details)

        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)

            if form.is_valid():
                print('form is valid')
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user_id = request.user.id
                data.save()


                messages.success(request , 'Thank you , Your review has been Submitted')
                return redirect(product_details)



    return 










def store(request , category_slug = None):
    categories = None
    products = None
    logo = Logo.objects.get(name = 'entrega')

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        products = Products.objects.filter(category = categories , is_available = True)
        page = request.GET.get('page')
        paginator = Paginator(products , 1)
        paged_product = paginator.get_page(page)
    else:
        products = Products.objects.all().filter(is_available = True).order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(products , 1)
        paged_product = paginator.get_page(page)

    
    context = {
        'products':paged_product,
        'logo' : logo,
        
    }
    return render(request , 'store.html', context)


 


def product_details(request , category_slug , product_slug):
    try:
        logo = Logo.objects.all()
        products = Products.objects.all().filter(is_available = True)
        single_product = Products.objects.get(category__slug= category_slug  , slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request) , product = single_product).exists()
    except  Exception as e:
        raise e

    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
        'products' : products,
        'logo' :logo,
    }
    
    return render(request , 'product-detail.html' , context) 