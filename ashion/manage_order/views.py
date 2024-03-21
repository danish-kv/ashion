from django.shortcuts import render, redirect
from django.contrib import messages
from user_profile.models import Address
from .models import *
from logintohome.models import Customer
from manage_cart.models import Cart
from django.views.decorators.cache import never_cache
from  manage_product.models import Variant
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from user_profile.models import Wallet_User
from decimal import Decimal
# Create your views here.



@login_required(login_url='adminlogin')
def manage_order(request):
    if 'email' in request.session:
        return redirect('error_page')
    
    orders = OrderedProducts.objects.all().exclude(Q(status = 'Cancelled') | Q(status = 'Returned')).order_by('-id')
    context = { 'order' : orders }
    return render(request,'admin_order.html',context)


@login_required(login_url='adminlogin')
def order_details_view(request,id):
    if 'email' in request.session:
        return redirect('error_page')

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
            obj.status = order_status
            
        except:
            order_status = None

        if order_status == 'Delivered':
            obj.delivery_date = timezone.now().date()

        if order_status == 'Cancelled':
            if obj.order_id.payment_method == 'cod':
                CancelledOrder.objects.create(
                    order_id = obj,
                    user_id = obj.user.id,
                    cancel_reason = 'Admin Cancelled'
                )
            elif obj.order_id.payment_method == 'Razor pay' or obj.order_id.payment_method == 'Wallet':
                
                try:
                    discount_amount = 0
                    if obj.order_id.coupon_id:
                        discount_amount = obj.order_id.coupon_id.discount_amount

                    
                    total_products = obj.order_id.orderedproducts_set.count()
                    refund_amount = discount_amount / total_products
                    print(f'{total_products} total products, {refund_amount} refund_amount ')

                    # refunding amount
                    amount = obj.total_amount - Decimal(refund_amount)
                    print(amount)
                    print( obj.total_amount)
                    print(obj.quantity)
                    print( refund_amount)
                    wallet_user = Wallet_User.objects.filter(user_id = obj.user).order_by('-id').first()
                    if not wallet_user:
                        balance = 0
                    else:
                        balance = wallet_user.balance
                    new_balance = balance + amount
                    Wallet_User.objects.create(
                        user_id = obj.user,
                        transaction_type = "Credit",
                        amount = amount,
                        balance = new_balance
                    )

                except Exception as e:
                    print(e)
                    messages.error(request,f'Facing some issues {str(e)}')
                pro = Variant.objects.get(product_id = obj.product.product_id, id=obj.product.id )
                pro.stock = pro.stock + obj.quantity
                obj.save()
                pro.save()
                obj.status = 'Cancelled'
                obj.save()
                CancelledOrder.objects.create(
                    order_id = obj,
                    user_id = obj.user,
                    cancel_reason = 'Admin Cancelled'
                )

        messages.success(request,f'Order status changed to {order_status}')
        return redirect('order_deatils_view',id)
    

@login_required(login_url='adminlogin')
def cancelled_orders(request):
    if 'email' in request.session:
        return redirect('error_page')

    data = CancelledOrder.objects.all()
    context = { 'data' : data }
    return render(request,'cancel_request.html',context)

@login_required(login_url='adminlogin')
def order_return(request):
    if 'email' in request.session:
        return redirect('error_page')
    
    data = OrderReturns.objects.all()
    context = { 'data' : data }
    return render(request,'order_return.html',context)