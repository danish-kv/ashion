from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from logintohome.models import Customer
from .models import *
from datetime import datetime


# Create your views here.

def AdminLogin(request):
    if request.user.is_authenticated:
        return redirect('AdminHome')

    
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password = request.POST.get('password')

        admin = authenticate(username=username1, password=password)

        if admin is not None:
            login(request, admin)  
            return redirect('AdminHome')
        else:
            messages.error(request, 'Username or password is invalid')
            return render(request,'admin_login.html')
        
    return render(request, 'admin_login.html')



@login_required(login_url='adminlogin')
def AdminHome(request):
    return render(request, 'admin_home.html')




@never_cache
def AdminLogout(request):
    logout(request)  
    return redirect('adminlogin')




@login_required(login_url='adminlogin')  
def manage_user(request):
    data = Customer.objects.all()
    context = {'data' : data}
    return render(request,'user_manage.html',context)




@never_cache 
def Blockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = True
    user.save()
    return redirect('manageuser')




@never_cache
def Unblockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = False
    user.save()
    return redirect('manageuser')






def product_offers(request):
    offers = Product_Offer.objects.all()
    product = products.objects.all()


    context = { 'offers' : offers,
               'products': product }

    return render(request,'product_offers.html',context)


def add_product_offers(request):

    if request.method == 'POST':
        pro_id = request.POST.get('productName')
        print(pro_id)
        percentage = request.POST.get('percentage')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            product = products.objects.get(id=pro_id)

            if not 1 <= float(percentage) < 100:
                messages.error(request, 'Percentage must be between 1 and 100.')
                return redirect('product_offers')
            
            percentage = float(percentage)
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if end_date < start_date:
                messages.error(request, 'End date must be after start date.')
                return redirect('product_offers')


            offers = Product_Offer(
                product_id = product,
                percentage = percentage,
                start_date = start_date,
                end_date = end_date,
            )
            offers.save()

            messages.success(request,f"'{product}' added '{percentage}%' offer ")
            return redirect('product_offers')
        
        except products.DoesNotExist:
            messages.error(request, 'Invalid product selected.')

    return redirect('adminlogin')


    
def edit_product_offers(request,id):
    offer = Product_Offer.objects.get(id=id)
    if request.method == 'POST':
        percentage = request.POST.get('percentage')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            offer = Product_Offer.objects.get(id=id)

            

            if not 0 <= float(percentage) <= 100:
                messages.error(request, 'Percentage must be between 0 and 100.')
                return redirect('product_offers')
            
            percentage = float(percentage)
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if end_date < start_date:
                messages.error(request, 'End date must be after start date.')
                return redirect('product_offers')

    

            offer.percentage = percentage
            offer.start_date = start_date
            offer.end_date = end_date
            offer.save()

            messages.success(request,f"'{offer}' Updated with '{percentage}%' offer ")
            return redirect('product_offers')
        
        except products.DoesNotExist:
            messages.error(request, 'Invalid product selected.')

    return render(request,'product_offers.html')


def product_offer_status(request,id):
    status = Product_Offer.objects.get(id = id)

    if status.is_active == True:
        status.is_active = False
        status.save()
        messages.success(request,'Status changed')
        return redirect('product_offers')
    else:
        status.is_active = True
        status.save()
        messages.success(request,'Status changed')
        return redirect('product_offers')


def category_offers(request):

    offers = Category_Offer.objects.all()
    category = Category.objects.all()

    context = { 'offers' : offers,
               'categories' : category }

    return render(request,'category_offers.html',context)






def add_category_offers(request):

    if request.method == 'POST':
        cat_id = request.POST.get('CategoryName')
        print(cat_id)
        category = Category.objects.get(id=cat_id)
        percentage = request.POST.get('percentage')

        offers = Category_Offer(
            category_id = category,
            percentage = percentage
        )
        offers.save()
        messages.success(request,f"'{category}' added '{percentage}%' offer ")
        return redirect('category_offers')

    return redirect('adminlogin')


def edit_category_offers(request,id):
    offer = Category_Offer.objects.get(id=id)
    if request.method == 'POST':
        percentage = request.POST.get('percentage')

        offer.percentage = percentage
        offer.save()
        messages.success(request,'Offer Updated')
        return redirect('category_offers')

    return render(request,'category_offers.html')


def category_offer_status(request,id):
    status = Category_Offer.objects.get(id = id)

    if status.is_active == True:
        status.is_active = False
        status.save()
        messages.success(request,'Status changed')
        return redirect('category_offers')
    
    else:
        status.is_active = True
        status.save()
        messages.success(request,'Status changed')
        return redirect('category_offers')