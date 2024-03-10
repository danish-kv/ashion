from django.shortcuts import render, redirect
from django.contrib import messages
from user_profile.models import Address
from .models import *
from logintohome.models import Customer
from manage_cart.models import Cart
from django.views.decorators.cache import never_cache
from  manage_product.models import Variant
from django.db.models import Q
# Create your views here.




def manage_order(request):
    orders = OrderedProducts.objects.all().exclude(Q(status = 'Cancelled') | Q(status = 'Returned'))
    context = { 'order' : orders }
    return render(request,'admin_order.html',context)


def order_details_view(request,id):
    orders = OrderedProducts.objects.get(id=id)
    context = { 'obj' : orders }
    return render(request,'admin_order_details.html',context)


def change_order_status(request,id):
    try:
        obj = OrderedProducts.objects.get(id=id)
    except: obj = None
    
    if request.method == 'POST':
        try:
            order_status = request.POST.get('statusRadio')
        except: order_status = None

        obj.status = order_status
        obj.save()
        messages.success(request,f'Product {order_status}')
        return redirect('order_deatils_view',id)
    


def cancelled_orders(request):
    data = CancelledOrder.objects.all()
    context = { 'data' : data }
    return render(request,'cancel_request.html',context)


def order_return(reqesut):
    data = OrderReturns.objects.all()
    context = { 'data' : data }
    return render(reqesut,'order_return.html',context)