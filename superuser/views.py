from itertools import product
from django.shortcuts import render,get_object_or_404,redirect
from advertisemennt.models import Logo
from order.models import Order, OrderProduct, Payment
from store.models import Offers, Products
from django.contrib import messages
from .forms import Offerform, Productform, Statusform
from category.forms import CategoryForm
from accounts.models import Account
from category.models import Category
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
# Create your views here.





def offer_update(request , id):

    offer = Offers.objects.get(id = id)
    form = Offerform(instance=offer)
    product = Products.objects.all()
    category = Category.objects.all()

    if request.method == 'POST':
        form  = Offerform(request.POST , instance=offer)

        if form.is_valid():
            print('Offer Update is valid')

            form.save()
            return redirect('admin-offer')
        else:
            print('offer update form is not valid')
            messages.error(request , 'Please check the details')
            return redirect(offer_update)
    else:
        print('Form is not valid')
        messages.error(request, 'Details is not valid please check it!!!')

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'offer' : offer,
        'product':product,
        'category' : category,
        'logo' : logo,
        'first_name' : first_name,
    }


    return render(request , 'superuser/admin-offer-update.html' , context)









@login_required(login_url='admin-login')
def offer_add(request):

    form = Offerform()

    if request.method == 'POST':
        form = Offerform(request.POST)
        print(form)
        if form.is_valid():
            print('offer form is valid')
            form.save()
            return redirect(offer)
        else:
            print('offer is not valid')
            messages.error(request, 'Please check the details')
            return redirect(offer_add)
    logo = Logo.objects.get(name='entrega')
    category = Category.objects.all()
    product = Products.objects.all()

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'category' : category,
        'product' : product,
        'logo' : logo,
        'first_name' : first_name,
    }
    return render(request , 'superuser/admin-offer-add.html' , context)






@login_required(login_url='admin-login')
def offer_delete(request , id):

    offers = Offers.objects.get(id =  id)

    if request.method == 'POST':
        offers.delete()
        print('offer deleted successfully')
        return redirect(offer)





@login_required(login_url='admin-login')
def offer(request):

    offer = Offers.objects.all()
    logo = Logo.objects.get(name='entrega')

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'offer' : offer,
        'logo' : logo,
        'first_name' : first_name,
    }


    return render(request , 'superuser/admin-offer.html', context)






@login_required(login_url='admin-login')
def admin_update_status(request , id ):
    
    order_id = id

    print(order_id)

    

    status = Order.objects.get(order_number = order_id)

    print(status)

    form = Statusform(instance=status)

    

    if request.method == 'POST':
        form = Statusform(request.POST , instance = status)

        if form.is_valid():
            print('Form is Valid')

            form.save()
            return redirect(admin_order)
        else:
            print('Form is Invalid')
            messages.error(request , 'Details is not valid please check it!!')

    else:
        print('Form is Not Valid')
        messages.error(request , 'Details is not valid please check it!!')

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'status': status,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-status.html' ,context)
    


@login_required(login_url='admin-login')
def admin_order(request):
    order_product = OrderProduct.objects.all()
    status = Order.objects.all()

    p = Paginator(Account.objects.all() , 10)
    page = request.GET.get('page')
    paginator = p.get_page(page)

    sub_total = 0 
    
    for i in order_product:
        sub_total += i.product_price * i.quantity + i.order.tax

    

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'order_product' : order_product,
        'sub_total'     : sub_total,
        'logo' : logo,
        'first_name' : first_name,
        'paginator':paginator,
        'status' : status,

    }

    return render (request , 'superuser/admin-order.html' , context)






@login_required(login_url='admin-login')
def admin_product_list(request , category_slug=None):
    
    categories = None
    products = None
    

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        products = Products.objects.filter(category = categories , is_available = True)
        page = request.GET.get('page')
        paginator = Paginator(products , 1)
        paged_product = paginator.get_page(page)
    else:
        products = Products.objects.all().filter(is_available = True).order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(products , 10)
        paged_product = paginator.get_page(page)




    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'product' : paged_product,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-product-list.html' , context)

@login_required(login_url='admin-login')
def admin_category_add(request):

    if request.method == 'POST':
        print('posted success')
        form = CategoryForm(request.POST , request.FILES)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect(admin_category)
        else:
            messages.error(request , 'Catergory already existed!!')
            print('form is invalid')
            return redirect(admin_category_add)

    form = CategoryForm()
    category = Category.objects.all()
    
    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'category': category,
        'logo' : logo,
        'first_name' : first_name,
    }


    return render(request , 'superuser/admin-category-add.html' , context)






@login_required(login_url='admin-login')
def admin_category_delete(request , id):
    category = Category.objects.get(id = id )
    print(category)
    if request.method == 'POST':
        category.delete()
        print('Category deleted successfully')
        return redirect(admin_category)
    

@login_required(login_url='admin-login')
def admin_category_update(request , id):
    category_id = id
    category = Category.objects.get(id = category_id)
    print(category)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST , request.FILES , instance = category)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect(admin_category)
        else:
            print('Form is Invalid')
            messages.error(request , 'Details is not valid please check it!!')

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'category' : category,
        'logo' : logo,
        'first_name' : first_name,
    }
    return render(request , 'superuser/admin-category-update.html' , context)



@login_required(login_url='admin-login')
def admin_category(request , category_slug=None):


    categories = None
    

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        category = Category.objects.filter(category = categories , is_available = True)
        page = request.GET.get('page')
        paginator = Paginator(category , 1)
        paged_product = paginator.get_page(page)
    else:
        category = Category.objects.all().order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(category , 15)
        paged_product = paginator.get_page(page)

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'category' : paged_product,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-category.html' , context)


@login_required(login_url='admin-login')
def admin_user_block(request , id):
    user = Account.objects.get(id = id)
    print(user)
    if user.is_active:
        user.is_active = False
        user.save()
        print('user blocked')
    else:
        user.is_active = True
        user.save()
        print('user unblocked')
    return redirect(admin_user_list)




@login_required(login_url='admin-login')
def admin_user_list(request , category_slug=None):

    

    #set up pagination
    categories = None
    

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        category = Account.objects.filter(category = categories , is_available = True)
        page = request.GET.get('page')
        paginator = Paginator(category , 1)
        paged_product = paginator.get_page(page)
    else:
        account = Account.objects.all().order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(account , 15)
        paged_product = paginator.get_page(page)

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'account' : paged_product,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-user-list.html' , context)






@login_required(login_url='admin-login') 
def admin_home(request):


    first_name = request.user.first_name

    products = Products.objects.all()
    order = OrderProduct.objects.all()


    cod = Payment.objects.filter(payment_method = 'COD').count()
    paypal = Payment.objects.filter(payment_method = 'Paypal').count()

    """ order status count """

    ready = Order.objects.filter(status = 'Ready for Shipping').count()
    shipped = Order.objects.filter(status = 'Shipped').count()
    out = Order.objects.filter(status = 'Out for Delivery').count()
    delivered = Order.objects.filter(status = 'Delivered').count()
    cancelled = Order.objects.filter(status = 'Cancelled').count()

    status = ['Ready to Ship' , 'Shipped' , 'Out for Delivery' , 'Delivered' , 'Cancelled'] 
    status_no = [ready , shipped , out , delivered , cancelled]




    user = Account.objects.all()
    user_count = user.count()
    print(user_count)

    

    sub_total = 0
    for i in order:
        sub_total += i.product_price * i.quantity + i.order.tax

    order_count = order.count()

    print(f"Order count :  {order_count}")
    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name
    context = {
        'products' : products,
        'order_count' : order_count,
        'sub_total' : sub_total,
        'user_count' : user_count,
        'cod' : cod,
        'paypal':paypal,
        'status': status,
        'status_no' : status_no,
        'logo' : logo,
        'user' :first_name,

    }

    return render(request , 'superuser/admin-home.html' , context)




@login_required(login_url='admin-login')
def admin_product_update(request ,id ):
    product_id = id
    products = Products.objects.get(id = product_id)
    form = Productform(instance=products)

    if request.method == 'POST':
        form = Productform(request.POST , request.FILES , instance =products)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect(admin_home)
        else:
            print('Form is not valid')
            messages.error(request, 'Details is not valid please check it!!')
            return redirect(admin_product_update)
    form = Productform(instance = products)
    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name
    context = {
        'form' : form,
        'products' : products,
        'product_id': product_id,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-product-update.html', context)




@login_required(login_url='admin-login')
def admin_product_delete(request , id):
    products = Products.objects.get(id=id)
    print(products)
    if request.method == 'POST':
        products.delete()
        print('deleted successfully')
        return redirect(admin_product_list)
    



@login_required(login_url='admin-login')
def admin_product(request):
    
    if request.method == 'POST':
        print('posted success')
        form = Productform(request.POST , request.FILES)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect(admin_product_list)
        else:
            print(form.errors)
            messages.error(request , 'Details is not valid please check it!!')
            print('form is invalid')
            return redirect(admin_product)
    else:
        form = Productform()

    logo = Logo.objects.get(name='entrega')
    first_name = request.user.first_name

    context = {
        'form' : form,
        'logo' : logo,
        'first_name' : first_name,
    }

    return render(request , 'superuser/admin-product.html' , context)


@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request , email = email , password = password)
        print(user)
        if user is not None:
            user = Account.objects.get(email=email)
            if user.is_admin == True:
                login(request , user)
            else:
                messages.error(request , 'User is not found')
                return redirect(admin_login)
        else:
            messages.error(request , 'User is not found')
            print('user is none')


    return render(request , 'superuser/admin-login.html')


def admin_logout(request):
    
    if request.user.is_authenticated:
        logout(request )
        return redirect(admin_login)











