from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from manage_product.models import products
from manage_category.models import Category
from datetime import datetime
from django.utils import timezone
from . import models
from django.core.paginator import Paginator
from user_profile.models import Wallet_User
from decimal import Decimal
from django.contrib.auth.hashers import make_password

# Create your views here.


def home(request):
    data = request.GET.get('data', '')

    obj = products.objects.filter(is_listed=True)[:8]

    if data == 'all':
        obj = products.objects.filter(is_listed=True)[:8]
    elif data == 'Women':
        obj = products.objects.filter(category__name='Women', is_listed=True)[:8]
    elif data == 'Men':
        obj = products.objects.filter(category__name='Men', is_listed=True)[:8]
    elif data == 'Kids':
        obj = products.objects.filter(category__name='Kids', is_listed=True)[:8]
    else:
        obj = products.objects.filter(is_listed=True)[:8]

    new_products = products.objects.order_by('id')[:8]

    context = {"new_products": new_products,
               'data': obj,
               'user' :request.user if 'email' in request.session else None}
    
    return render(request, 'home.html', context)






def login(request):
    if 'email' in request.session :
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        
        
        try:
            user = Customer.objects.get(email = email,password = password)
        except Customer.DoesNotExist:
            user = None

        if password.strip() == "":
            messages.error(request,'Please enter your password')
            return redirect(login)


        if user is not None:
            if user.is_blocked:
                messages.error(request,f'{email} is Blocked')
                return render(request,'login.html')


            if user.is_verified:
                request.session['email'] = email
                messages.success(request,'welcome to ashion')
                return redirect('home')
            else:
                otp = models.generate_otp(user)
                models.send_otp_email(user,otp)
                return redirect('otpverify',user.id)
        else:
            messages.error(request, 'Invalid email or password')
            
    return render(request, 'login.html')


def signup(request):
    if 'email' in request.session :
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        date_joined=timezone.now().date()
        referral_code = request.POST.get('ref_code',None)


        if username.strip() == "":
            messages.error(request,'Please enter your Username')
            return redirect(signup)
        
        if number.strip() == "":
            messages.error(request,'Please enter your Phone Numebr')
            return redirect(signup)
        
        if password1.strip() == "":
            messages.error(request,'Please enter your Password')
            return redirect(signup)
        
        if password2.strip() == "":
            messages.error(request,'Please enter your Confirm Password')
            return redirect(signup)

        if password1 != password2:
            messages.error(request,'Both password is not same!')
            return redirect('signup')
        
        if len(password1) < 6:
            messages.error(request,'Password should be at least 6 charaters')
            return redirect('signup')
        
        if len(number) != 10:
            messages.error(request,'Phone number should be 10 digits')
            return redirect('signup')

        if Customer.objects.filter(number=number).exists():
            messages.error(request,'Number is already Exists')
            return redirect('signup')
        
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('signup')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('signup')
        


        user = Customer(username=username,
                        number=number,
                        email=email,
                        password= password1,
                        date_joined=date_joined
                        )
        user.save()
        
        # new_user_wallet = Wallet_User(user_id =user.id)
        

        if referral_code:
            reffered_get_amount = 271
            new_user_get_amount = 101
            reffered_user = Customer.objects.get(referral_code = referral_code)
            print(f'{reffered_user} checkkkkkk')

            reffered_wallet = Wallet_User.objects.filter(user_id = reffered_user.id).order_by('-id').first()

            if reffered_wallet:
                new_balance = reffered_wallet.balance + reffered_get_amount
                print(new_balance, reffered_wallet.amount,reffered_wallet.balance, reffered_get_amount)
            else:
                new_balance = reffered_get_amount

            #reffered user
            Wallet_User.objects.create(
                user_id = reffered_user,
                transaction_type = "Refferel Bonus",
                amount = float(reffered_get_amount),
                balance = float(new_balance)
                )
            print(f"Refferel Bonus: {reffered_user, reffered_get_amount, new_balance}")
            
            #new user
            Wallet_User.objects.create(
                user_id = user,
                transaction_type = "Signup Refferal Bonus",
                amount = new_user_get_amount,
                balance = new_user_get_amount
                )
            print(f"Signup Refferal Bonus: {user, new_user_get_amount, new_user_get_amount}")

        return redirect('otpverify', id=user.id)
    return render(request,'signup.html')




def otp_verification(request,id):
    user = None
    if request.method == "POST":
        user1 = Customer.objects.get(id = id)
        userotp = user1.otp_field
        entered_otp = request.POST.get('otp')

        if entered_otp.strip() == "":
            messages.error(request,'Please enter your OTP')
            return redirect(signup)

        userotp = int(userotp)
        entered_otp = int(entered_otp)

        if userotp == entered_otp:
            user2 = Customer.objects.get(id=id)
            user2.is_verified = True
            user2.save()
            messages.success(request,'Your Emaill is Verified')
            return redirect(login)
        
        else:
            messages.error(request,'Invalid OTP, Please Try again')
            return redirect('otpverify', id=id)
        
            # Retrieve user for 'GET' request
    try:
        user = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('home')
        
    return render(request, 'otp_verification.html',{'user': user})






def logout(request):
    if 'email' in request.session:
        
        del request.session['email']
        
        messages.success(request,'You have been successfully logged out. Thank you for using our services!')
        return  redirect('home')
    




def contact(request):
    return render(request,'contact.html')