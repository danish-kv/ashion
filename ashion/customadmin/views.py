from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from logintohome.models import Customer
from .models import *
from datetime import datetime, timedelta
from manage_order.models import *
from django.utils import timezone
from django.db.models import Q, Sum, Count
import json
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

    orders = OrderedProducts.objects.filter(status = "Delivered" )

    user = Customer.objects.filter(is_verified = True, is_blocked=False)
    orders_count = orders.count()
    user_count = user.count()



    total_amount = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    delivered_orders = Order.objects.filter(orderedproducts__in=orders)
    payment_methods = delivered_orders.values('payment_method').annotate(total_orders=Count('id'))

    categories = Category.objects.annotate(total_sales=Count('products__variant__product_id__category')).values('name', 'total_sales')


    print(categories)
    print(orders)
    print(f"count :{orders_count}")
    print(total_amount)
    print(payment_methods)



    top_products = orders.values('product__product_id__name').annotate(total_sales=Count('product')).order_by('-total_sales')[:10]()
    top_categories = Category.objects.annotate(total_ordered_products=Count('products__variant__product_id__category')).order_by('-total_ordered_products').values('name', 'total_ordered_products')[:10]


    context = { 'orders_count' : orders_count,
               'total_amount' : total_amount,
               'user_count' : user_count,
 
               }

    
    return render(request, 'admin_home.html', context)



    # end_date = datetime.now()
    # start_date = end_date - timedelta(days=7)
    # print(start_date, end_date)



@never_cache
def AdminLogout(request):
    if request.user.is_authenticated:

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





@login_required(login_url='adminlogin')
def product_offers(request):
    offers = Product_Offer.objects.all()
    product = products.objects.all()


    context = { 'offers' : offers,
               'products': product }

    return render(request,'product_offers.html',context)


@login_required(login_url='adminlogin')
def add_product_offers(request):

    if request.method == 'POST':
        pro_id = request.POST.get('productName')
        # print(pro_id)
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

            if Product_Offer.objects.filter(product_id=product).exists():
                messages.error(request,f'Offer Already exists with "{product}"')
                return redirect('product_offers')

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


@login_required(login_url='adminlogin')
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



@login_required(login_url='adminlogin')
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


@login_required(login_url='adminlogin')
def category_offers(request):

    offers = Category_Offer.objects.all()
    category = Category.objects.all()

    context = { 'offers' : offers,
               'categories' : category }

    return render(request,'category_offers.html',context)





@login_required(login_url='adminlogin')
def add_category_offers(request):

    if request.method == 'POST':
        cat_id = request.POST.get('CategoryName')
        percentage = request.POST.get('percentage')
        print(cat_id)

        try:
            category = Category.objects.get(id=cat_id)

            if Category_Offer.objects.filter(category_id=category).exists():
                messages.error(request,f'Offer already Exists with "{cat_id}"')
                return redirect("category_offers")
            
            if not 0 <= float(percentage) <= 100:
                messages.error(request, 'Percentage must be between 0 and 100.')
                return redirect('product_offers')
            
            percentage = float(percentage)


            offers = Category_Offer(
                category_id = category,
                percentage = percentage
            )
            offers.save()
            messages.success(request,f"'{category}' added '{percentage}%' offer ")
            return redirect('category_offers')
        
        except products.DoesNotExist:
            messages.error(request, 'Invalid Category selected.')

    return redirect('adminlogin')


@login_required(login_url='adminlogin')
def edit_category_offers(request,id):
    offer = Category_Offer.objects.get(id=id)
    if request.method == 'POST':
        percentage = request.POST.get('percentage')


        if not 0 <= float(percentage) <= 100:
            messages.error(request, 'Percentage must be between 0 and 100.')
            return redirect('category_offers')
            
        percentage = float(percentage)

        offer.percentage = percentage
        offer.save()

        messages.success(request,'Offer Updated')
        return redirect('category_offers')

    return render(request,'category_offers.html')



@login_required(login_url='adminlogin')
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
    

@login_required(login_url='adminlogin')
def sales_report(request):
    orders = None
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        

        print(f"Start Date: {start_date}, End Date: {end_date}")
        
        orders = OrderedProducts.objects.filter(status ='Delivered', delivery_date__range=(start_date, end_date))
        print(orders)

    date_of_download = timezone.now()

    context = { 'orders' : orders,
                'date_of_download' : date_of_download
                  }
    
    return render(request,'sales_report.html', context)



# # views.py
# from django.db.models import Count, Sum
# from django.utils import timezone
# from datetime import datetime, timedelta

# @login_required(login_url='adminlogin')
# def AdminHome(request):
#     # Calculate date range for the last 12 months
#     end_date = timezone.now()
#     start_date = end_date - timedelta(days=365)

#     # Monthly orders
#     monthly_orders = OrderedProducts.objects.filter(
#         created_at__gte=start_date, created_at__lte=end_date
#     ).extra({'month': "EXTRACT(month FROM created_at)"}).values('month').annotate(order_count=Count('id'))

#     # Monthly new users
#     monthly_new_users = Customer.objects.filter(
#         date_joined__gte=start_date, date_joined__lte=end_date
#     ).extra({'month': "EXTRACT(month FROM date_joined)"}).values('month').annotate(user_count=Count('id'))

#     # Monthly amount sales
#     monthly_amount_sales = OrderedProducts.objects.filter(
#         created_at__gte=start_date, created_at__lte=end_date
#     ).extra({'month': "EXTRACT(month FROM created_at)"}).values('month').annotate(total_sales=Sum('total_amount'))

#     return render(request, 'admin_home.html', {
#         'monthly_orders': monthly_orders,
#         'monthly_new_users': monthly_new_users,
#         'monthly_amount_sales': monthly_amount_sales,
#     })
