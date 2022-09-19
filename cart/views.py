from math import prod
from django.shortcuts import render , redirect,get_object_or_404
from accounts.models import Offer
from cart.forms import AddressForm
from cart.models import AddressUser, Cart, CartItem
from store.models import Products, variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from advertisemennt.models import Logo

# Create your views here.

def update_cart(request):
    if request.method ==  "POST":
        product_id = int(request.POST.get('product_id'))
        if (CartItem.objects.filter(user = request.user , product_id = product_id)):
            product_qty = int(request.POST.get('product_qty'))
            cart_item = CartItem.objects.get(product_id = product_id , user = request.user)
            cart_item.quantity = product_qty

            cart_item.save()

            return JsonResponse({'status' : 'Updated successfully'})




@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None,):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            address = AddressUser.objects.filter(user = request.user.id)
            print(address)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    address = AddressUser.objects.filter(user = request.user.id)
    logo = Logo.objects.get(name = 'entrega')
   
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'address' : address ,
        'grand_total' : grand_total,
        'logo' : logo,
        
    }
    return render(request, 'store/checkout.html', context)






def remove_cart_item(request, product_id):
    product = get_object_or_404(Products , id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product , user = request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product , cart = cart)

    cart_item.delete()
    return redirect('cart')




def remove_cart(request , product_id ):
    
    product = get_object_or_404(Products ,id= product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product , user = request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product , cart = cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect(carts)


def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Products.objects.get(id=product_id)

    if current_user.is_authenticated:
        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value =request.POST[key]

                try:
                    variations = variation.objects.get(product=product , variations_category__iexect = key , variations_value__iexect = value)
                    product_variations.append(variations)
                except:
                    pass 



        is_cart_item_exists = CartItem.objects.filter(product=product , user = current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product = product , user = current_user)

            ex_var_list =[]

            id = []

            for item in cart_item:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            print(ex_var_list)


            if product_variations in ex_var_list:
                index = ex_var_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product = product , quantity = 1 , user = current_user)
                if len(product_variations) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variations)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1 ,
                user = current_user 
                )
            if len(product_variations) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)
            cart_item.save() 
            
        return redirect(carts)

    #if the user is not authenticated
    else:
        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value =request.POST[key]

                try:
                    variations = variation.objects.get(product=product , variations_category__iexect = key , variations_value__iexect = value)
                    product_variations.append(variations)
                except:
                    pass 


        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create( cart_id = _cart_id(request))
            cart.save()


        is_cart_item_exists = CartItem.objects.filter(product=product , cart = cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product = product , cart = cart)

            ex_var_list =[]

            id = []

            for item in cart_item:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            print(ex_var_list)


            if product_variations in ex_var_list:
                index = ex_var_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product = product , quantity = 1 , cart = cart)
                if len(product_variations) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variations)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1 ,
                cart = cart 
                )
            if len(product_variations) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)
            cart_item.save() 
            
        return redirect(carts)

def carts(request, total=0, cart_items=None, quantity=0):

    try:
        tax=0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user , is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        print('cart object does not exist')
        pass
    
    tax_amount = round(float(total) * float(0.5/100),2)
    sub_total = round(float(total)+tax_amount, 2)
    logo = Logo.objects.get(name = 'entrega')
    context = {
        'total':total ,
        'quantity': quantity ,
        'cart_items' : cart_items,
        'tax_amount' : tax_amount ,
        'sub_total' : sub_total ,
        'logo' :logo
    }
    return render(request, 'store/cart.html', context)  
