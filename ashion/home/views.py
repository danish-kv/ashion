from django.shortcuts import render, redirect

from django.contrib import messages
from django.db.models import Q
from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate, login
from manage_product.models import products, Variant
from manage_category.models import Category
from django.core.paginator import Paginator
from django.db.models import Max
from .models import Wishlist
from logintohome.models import Customer
from django.urls import reverse
from customadmin.models import Product_Offer
# Create your views here.



def product_list(request):
    context ={}
    product_list = products.objects.filter(is_listed = True) 
    pro_offer = Product_Offer.objects.filter(is_active=True)
    print(pro_offer)

    data = request.GET.get('data')
    print(data)

    if data == 'Women':
        product_list = product_list.filter(category__name= data, is_listed=True)
        
        context['data'] = 'Women'
    elif data == 'Men':
        product_list = product_list.filter(category__name = data, is_listed=True)
        context['data'] = 'Men'
  

    elif data == 'Kids':
        product_list = product_list.filter(category__name = data, is_listed=True)
        context['data'] = 'Kids'


    sort_by = request.GET.get('sortby')

    if sort_by:
        product_list = product_list.order_by(sort_by)
        context['product_list'] = product_list


    
    page = 1
    if request.GET:
        page = request.GET.get('page',1)

    paginator = Paginator(product_list, 9)
    product_list = paginator.get_page(page)


    context['product'] = product_list  
    return render(request, 'product_list.html', context)







def product_details(request,id):
    product = products.objects.get(id = id)
    variants = Variant.objects.filter(product_id = id)
    print(product.id)
    var  = Variant.objects.filter(product_id = id).aggregate(m = Max('stock'))['m']
    print(var)
    category = Category.objects.filter(is_listed = True)

    context = {'product' : product,
               'variants': variants,
               "var":var,
               'cat' : category,
              }
    return render(request,'product_details.html',context)


def search(request):
    if request.method == "GET":
        search = request.GET.get('search')

        search_result = products.objects.filter(name__icontains = search)
        context = {'product' : search_result} 
        return render(request,'product_list.html',context)







def add_to_wishlist(request,id,from_page):
    if 'email' in request.session:
        email_id = request.session.get('email')
        

        try:
            user_id = Customer.objects.get(email=email_id)
            product_id = products.objects.get(id=id)
            
            if Wishlist.objects.filter(product_id = product_id).exists():
                messages.warning(request,'Product is already in your wishlist')
            else:
                Wishlist.objects.create(
                    user_id = user_id,
                    product_id = product_id,
                )
                messages.success(request,'Added to wishlist')


        except Customer.DoesNotExist:
            messages.error(request,'Customer not found')
        except products.DoesNotExist:
            messages.error(request,'Product not found')


        if from_page == 'product_details':
            return redirect('productdetails',id = id)
        elif from_page == 'home':
            return redirect('home')
        elif from_page == 'product_list':
            data = request.GET.get('data')
            if data:
                return redirect(reverse('productlist') + f'?data={data}')
            else:
                return redirect('productlist')

        else:
            return redirect('home')
    else:
        messages.error(request,'Please login for wishlisting a product')
        return redirect('login')


def wishlist(request):
    if 'email' in request.session:
        wish = Wishlist.objects.all()
        context = { 'wishlist' : wish }
        return render(request,'wishlist.html',context)
    
    messages.error(request,'Please login first')
    return redirect('login')


def remove_from_wishlist(request,id):
    wish = Wishlist.objects.get(id=id)
    wish.delete()
    messages.success(request,f"'{wish.product_id.name}' removed from wishlist")
    return redirect('wishlist')




def Search_Products(request):
    search_query = request.GET.get('query',' ')
    print(search_query)

    if search_query:
        result = products.objects.filter(name__istartswith = search_query)
    else:
        result = []

    context = { 'product' : result }

    return render(request,'product_list.html',context)
