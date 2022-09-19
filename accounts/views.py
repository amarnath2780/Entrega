from unicodedata import name
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from cart.models import AddressUser, Cart, CartItem
from advertisemennt.models import Add, IconAdd, Logo
from .forms import AddAdddressForm, RegistrationForm
from .models import Account, Offer, Turno
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from store.models import Products
from .otp import verify , verify_check
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required





@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact = request.user.email )

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request , 'password updateded successfully')
                logout(request)
                return redirect(user_home)
            else:
                messages.error(request , 'Please check the current password')
                return redirect(change_password)
        else:
            messages.error(request , 'Passwords does not match')
            return redirect(change_password)
        

    logo = Logo.objects.get(name='entrega')

    context = {
        'logo' : logo,
    }



    return render(request , 'authentication/change-password.html' , context)




@login_required(login_url="login")
def user_address(request):
    if request.method == 'POST':
        form = AddAdddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            messages.success(request,'Address added Successfully')
            return redirect('user_address')
    address = AddressUser.objects.filter(user = request.user)
    form = AddAdddressForm()
    context = {
        'form':form,
        'address':address
    }

    return render(request,'authentication/address.html',context)






def login_user_phone(request):
    
    if request.user.is_authenticated:
        return redirect(user_home)
    
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        print(mobile)
        password = request.POST.get('password')
        user = Account.objects.get(mobile=mobile)
        print(user)
        email = user.email
        user = authenticate(request, email = email, password = password)
        print(user)
    
        if user is not None:
            if user.is_verified:
                login(request,user)
                return redirect(user_home) 
            else:
                messages.error(request, 'Mobile Number is not verified. Please check your inbox..')
           
        else:
            messages.error(request, 'Invalid Credentials!')        
    return render(request,'login-phone.html')


def register_user_phone(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        phone_number = request.POST['mobile']
        request.session['mobile'] = phone_number    
        
        if form.is_valid():
            user = form.save(commit=False) 
          
            user.is_verified = False
            user.set_password(user.password)
            user.save()
            verify(phone_number)
            return render(request, 'authentication/otp.html',{'user':user})     
        else:
            messages.error(request, 'Invalid credentials..')
    else:
        form = RegistrationForm()
    logo = Logo.objects.get(name='entrega')
    context = {
        'form' : form,
        'logo' : logo,
    }
    return render(request, 'signup-phone.html',context)

def userotp(request):
    try:
        mobile=request.session['mobile']
        print(mobile)
        if request.method == 'POST':
            user=Account.objects.get(mobile = mobile)
            otp=request.POST['otp']
            print(otp)
            if verify_check(mobile,otp)==True:
                print(user)
                user.is_verified=True
                user.save()
                return redirect(user_home)
            else:
                messages.error(request,'otp entered is incorrect!')
    except:
        messages.error(request,'try again!')
        return redirect(userotp)            
    return render(request, 'authentication/otp.html')




def user_home(request):
    products = Products.objects.all().filter(is_available = True)
    add = Add.objects.all()
    icon = IconAdd.objects.all()
    logo = Logo.objects.get(name = 'entrega')
    char_1 = Offer.objects.get(name = 'character-1')
    char_2 = Offer.objects.get(name = 'character-2')
    char_3 = Offer.objects.get(name = 'character-3')
    about = Offer.objects.get(name = 'about')
    prize = Turno.objects.get(name= 'prize')
    winner_1 = Turno.objects.get(name= 'winner-1')
    winner_2 = Turno.objects.get(name= 'winner-2')
    context = {
        'products':products,
        'add' : add,
        'icon': icon,
        'logo' : logo,
        'char_1' :char_1,
        'char_2' :char_2,
        'char_3' :char_3,
        'about' : about,
        'prize' : prize,
        'winner_1' : winner_1,
        'winner_2' : winner_2,
    }


    return render(request, 'home.html',context )


def activate_user(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except( ValueError):  
        user = None
    if user and generate_token.check_token(user,token):
        user.is_verified = True
        user.save()
        return render(request, 'authentication/auth-success.html',{'user':user})  
    else:
        return render(request, 'authentication/activate-failed.html',{'user':user})

def send_verification_mail(request,user): 
    
    try:       
        current_site    = get_current_site(request)
        email_subject   = 'Activate your account'
        email_body      = render_to_string('authentication/activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user),
        })
        to_email = user.email 
        email = EmailMessage(  
                email_subject, email_body, to=[to_email]  
        )
        
        email.send() 
        print('email sent') 
        
    except:
        print('verification mail failed!')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
          
            user.is_verified = False
            user.set_password(user.password)
            user.save()
            
            send_verification_mail(request,user)
            return render(request, 'authentication/send-msg.html',{'user':user})     
        else:
            messages.error(request, 'Invalid credentials..')
            return redirect(register_user)
    else:
        form = RegistrationForm()
    logo = Logo.objects.get(name='entrega')
    context = {
        'form' : form,
        'logo' : logo
    }
    return render(request, 'signup.html',context)



def login_user(request):
    
    if request.user.is_authenticated:
        return redirect(user_home)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email = email, password = password)
    
        if user is not None:
            if user.is_verified:
                try:
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter( cart = cart).exists()
                    if is_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)
                        print(cart_items)

                        for item in cart_items:
                            item.user = user
                            item.save()

                except:
                    pass
                login(request,user)
                return redirect(user_home) 
            else:
                messages.error(request, 'Email is not verified. Please check your inbox..')
           
        else:
            messages.error(request, 'Invalid Credentials!')   

    logo = Logo.objects.get(name='entrega')

    context = {
        'logo' :logo
    }     
    return render(request,'login.html' , context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(login_user)






def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            
            """ Reset email password """
            current_site    = get_current_site(request)
            email_subject   = 'Reset Your Password'
            email_body      = render_to_string('authentication/reset_password.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user),
            })
            to_email = user.email 
            email = EmailMessage(  
                    email_subject, email_body, to=[to_email]  
            )
            
            email.send() 
            print('email send')


            messages.success(request, 'Password Reset Mail Has Been Sent To Your Email Address')
            return redirect(login_user)
        else:
            messages.error(request , 'Account does not exist')
            return redirect(forgot_password)
    logo = Logo.objects.get(name='entrega')

    context = {
        'logo' : logo,
    }
    return render(request , 'authentication/forgot_password.html' , context)



def resetpassword_validate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except( ValueError):  
        user = None
        return HttpResponse('OKay')

    if user and generate_token.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request , 'please reset your password')

        return redirect(resetpassword)
    else:
        messages.error(request , 'This link is have been Expired')
        return redirect(login_user)


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST.get('create_password')
        confirm_password = request.POST.get('confirm_password')
        print(f'password {password}')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request , 'Password reset Successful')

            return redirect(login_user)


            
        else:
            messages.error(request , 'Password do not match')
            return redirect(resetpassword)

    else:
        return  render(request , 'authentication/resetpassword.html')
    



