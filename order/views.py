from unicodedata import category
from django.shortcuts import render,redirect
from advertisemennt.models import Logo
from cart.models import AddressUser, CartItem , Cart
from category.models import Category
from order.forms import OrderForm
from order.models import Order, OrderProduct, Payment
import datetime
import razorpay
from django.conf import settings
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from store.models import Offers, Products
from datetime import date


# Create your views here.



def order_delete(request , id):
    current_user = request.user
    order = Order.objects.get(user = current_user , order_number = id)
    print(order)
    if request.method == "POST":
        order.delete()
        print('Order deleted Successfully')
        return redirect(order_list)

    








def order_list(request):
    current_user = request.user
    order_product = OrderProduct.objects.all().filter(user = current_user)
    order = Order.objects.all().filter(user= current_user)

    order_count = order_product.count()
    logo = Logo.objects.get(name='entrega')

    sub_total = 0 
    
    for i in order_product:
        sub_total += i.product_price * i.quantity + i.order.tax

    
    


    context = {
        'order_product' : order_product,
        'sub_total' : sub_total,
        'orders' :order,
        'order_count' : order_count,
        'logo':logo,
    }

    return render(request , 'order/order.html' , context)




def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number = order_number , is_ordered = True)

        order_product = OrderProduct.objects.filter(order_id = order.id)

        sub_total = 0 
        for i in order_product:
            sub_total += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id = transID)

        context = {
            'order' : order,
            'ordered_products' : order_product,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'sub_total' : sub_total,
            
        }
    except (Payment.DoesNotExist , Order.DoesNotExist):
        return redirect('store')




    return render (request , 'order/order_complete.html' , context)










def payments(request):
    body = json.loads(request.body)
    # store the transation details 
    order = Order.objects.get(user= request.user , is_ordered = False , order_number = body['orderID'])

    payment = Payment(
        user = request.user, 
        payment_id =body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()

    order.payment = payment
    order.is_ordered = True

    order.save()

    #move the cart_items to order product table 
    cart_items = CartItem.objects.filter(user = request.user)

    for item in cart_items:
        orderproduct = OrderProduct()

        orderproduct.order_id = order.id
        orderproduct.Payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        #Reduce the quantity of the sold products
        product = Products.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()




    #Clear cart 
    CartItem.objects.filter(user = request.user).delete()


    #send order recieved email to the customer
    email_subject   = 'Thank you for your order'
    email_body      = render_to_string('order/order_recieved_email.html',{
    'user': request.user,
    'order' : order,
    })
    to_email = request.user.email
    email = EmailMessage(  
            email_subject, email_body, to=[to_email]  
    )
    
    email.send() 
    print('email sent') 
        


    #send order number and transation id to sendData method 
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,

    }

    return JsonResponse(data)












def place_order(request , total=0, quantity=0):
    current_user = request.user
    print(f'user is {current_user}')
    # if the cart count is zero then redirect to cart 

    cart_items = CartItem.objects.filter(user = current_user)
    address = AddressUser.objects.filter(user = current_user)


    for cart_item in cart_items:
        category = cart_item.product.category
        product = cart_item.product
    


   
        



    print(category)

    print(cart_items)
    
    cart_count = cart_items.count()
    print(cart_count)

    if cart_count <= 0 :
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity) 
        quantity += cart_item.quantity
        
    tax = (2 * total)/100
    grand_total = total + tax 

    try:
        offer = Offers.objects.get(category = category)
        discount = (offer.offer)
    except Offers.DoesNotExist:
        discount = 0 

    
    totaly = (grand_total-(discount/100))

    print(totaly)


    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            print('form is valid')
            data               = Order()
            data.user          = current_user
            data.first_name    = form.cleaned_data['first_name']
            data.last_name     = form.cleaned_data['last_name']
            data.mobile        = form.cleaned_data['mobile']
            data.email         = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country       = form.cleaned_data['country']
            data.state         = form.cleaned_data['state']
            data.city          = form.cleaned_data['city']
            data.order_note    = form.cleaned_data['order_note']
            data.pincode       = form.cleaned_data['pincode']
            data.order_total   = totaly 
            data.tax           = tax
            data.save()


            

            #Generate order number 

            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)

            current_date = d.strftime("%y%m%d")

            print(current_date)

            order_number = current_date + str(data.id)          

            data.order_number = order_number

            data.save()

            payment_type = request.POST['payment']

            if payment_type == 'cod':
                print(data.id)
                data.order_number = order_number
                request.session['order_number'] = order_number
                print('COD')
                
                # store the transation details 
                order = Order.objects.get(user= request.user , is_ordered = False , order_number = order_number)

                payment = Payment(
                    user = request.user, 
                    payment_id =order_number,
                    payment_method = 'COD',
                    amount_paid = order.order_total,
                    status = 'Ready for Shipping',

                )
                payment.save()

                order.payment = payment
                order.is_ordered = True

                order.save()
            
                #move the cart_items to order product table 
                cart_items = CartItem.objects.filter(user = request.user)

                for item in cart_items:
                    orderproduct = OrderProduct()

                    orderproduct.order_id = order.id
                    orderproduct.Payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()


                    #Reduce the quantity of the sold products
                    product = Products.objects.get(id = item.product_id)
                    product.stock -= item.quantity
                    product.save()

                #Clear cart 
                CartItem.objects.filter(user = request.user).delete()


                #send order recieved email to the customer
                email_subject   = 'Thank you for your order'
                email_body      = render_to_string('order/order_recieved_email.html',{
                'user': request.user,
                'order' : order,
                })
                to_email = request.user.email
                email = EmailMessage(  
                        email_subject, email_body, to=[to_email]  
                )
                
                email.send() 
                print('email sent') 

                return redirect(order_complete)
                

            

            


            print(payment_type)
            order = Order.objects.get(user = current_user , is_ordered = False , order_number = order_number)
            client =  razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            DATA = {
                'amount' : data.order_total*100,
                'currency' : 'INR',
                'payment_capture' : 1,
            }

            payment =  client.order.create(data=DATA)
           

            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
                'discount' : discount,
                'address' : address,
                'payment' : payment ,
                'payment_type': payment_type,
            }

            return render (request , 'order/payments.html' , context)
        else:
            print('form is not valid')
    else:
        return redirect('checkout')
            



    return



