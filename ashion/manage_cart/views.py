from django.shortcuts import render, redirect
from .models import Cart
from manage_product.models import *
from logintohome.models import Customer
from django.contrib import messages
from user_profile.models import Address
from django.views.decorators.cache import never_cache
from .models import Checkout as checkout
from manage_order.models import *
from  manage_product.models import Variant
from manage_order.models import CancelledOrder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
# Create your views here.


#cart
def showcart(request):
    if 'email' in request.session:
        us_id = request.session.get('email')
        user = Customer.objects.get(email = us_id)

        cart = Cart.objects.filter(user_id = user)
        sub_total1 = 0
        
        for cart_product in cart:
            cart_product.pro_total = cart_product.size_variant.product_id.selling_price * cart_product.quantity                
            sub_total1 += cart_product.pro_total
        
        context = { 'cart_product' : cart,
                   'sub_total' : sub_total1 }
        return render (request,'cart.html',context)


    messages.error(request,'Frist you want to login...')
    return redirect('login')


#add to cart
def add_to_cart(request,id):
    if 'email' in request.session:
        if request.method == 'POST':
            us_id = request.session.get('email')
            user = Customer.objects.get(email = us_id)            
            size_id = request.POST.get('size')
            size_variant = Variant.objects.get(product_id=id, size=size_id)
            quantity = int(request.POST.get('quantity'))

            if size_variant.stock < quantity:
                messages.error(request,'Product is out of stock')
                return redirect('productdetails',id=id)
            
            if quantity > 5:
                messages.error(request,'Quantity must be less than 5')
                return redirect('productdetails',id=id)
            
            if Cart.objects.filter(size_variant = size_variant, user_id = user).exists():
                messages.error(request,'Product is already exists')
                return redirect('productdetails',id=id)
            
            Cart.objects.get_or_create(
                user_id = user,
                quantity = quantity,
                size_variant = size_variant,
            )

            messages.success(request,'Product added to cart')
            return redirect('productdetails',id = id)
            
    messages.error(request,'Frist you want to login...')
    return redirect('login.html')



def remove_from_cart(request,id):
    pro = Cart.objects.get(id=id)
    pro.delete()
    return redirect('cart')







def update_quantity(request):
    if request.method == 'POST' :
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        item = Cart.objects.get(id=product_id)
        print(product_id)

        if action == 'plus' and item.quantity < item.size_variant.stock and item.quantity < 5:
            item.quantity += 1
        elif action == 'minus' and item.quantity > 1:
            item.quantity -= 1

        item.sub_total = item.size_variant.product_id.selling_price * item.quantity
        item.save()

        return JsonResponse({'status': 'updated successfully'})
    else:
        return JsonResponse({'status': 'error'})



@never_cache
def Checkout(request):
    if 'email' in request.session:
        user_id = request.session.get('email')
        user = Customer.objects.get(email = user_id)
        addresses = Address.objects.filter(user = user, is_available=True)
        cart_items = Cart.objects.filter(user_id = user.id)
        sub_total1 =0
        for cart_product in cart_items:
            cart_product.pro_total = cart_product.size_variant.product_id.selling_price * cart_product.quantity                
            sub_total1 += cart_product.pro_total

        if user :
            checkout.objects.create(
                user_id = user.id,
                sub_total = sub_total1,
            )


        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment = client.order.create({ 'amount' : float(sub_total1) * 100, 'currency' : 'INR', 'payment_capture' : 1 })
        print('*************************************************')
        print(payment)
        print('*************************************************')

        context = { 'addresses' : addresses,
                   "cart_items" : cart_items,
                   'sub_total1' : sub_total1,
                   'cart' : cart_items,
                   'payment' :payment,
                   }
        return render(request,'checkout_page.html', context)
    return redirect('home')



# add address
@never_cache
def checkout_add_address(request):
    if 'email' in request.session:
        if request.method == 'POST':
            user_id = request.session.get('email')
            user = Customer.objects.get(email=user_id)
            name = request.POST.get('name')
            number = int(request.POST.get('number'))
            address  = request.POST.get('address')
            state = request.POST.get('state')
            district = request.POST.get('district')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            landmark = request.POST.get('landmark')

            if number < 10 and number > 10:
                messages.error(request,'Phone Number should be 10 digits')
                return redirect('add_address')
            if pincode != 6:
                messages.error(request,'Pincode should be 6 digits')
            
            data = Address(
                user = user,
                name = name,
                number = number,
                address = address,
                state = state,
                district = district,
                city = city,
                landmark = landmark,
                pincode = pincode
            )
            data.save()
            messages.success(request,f"'{name}'s Adderss saved")
            return redirect('checkout')


    return render(request,"checkout_address.html")










@never_cache
def place_order(request):

    if  'email' in request.session:
        user_id = request.session.get('email')
        user = Customer.objects.get(email = user_id)

        cart_objects = Cart.objects.filter(user_id=user)

        for cart_obj in cart_objects:
            if cart_obj.quantity > cart_obj.size_variant.stock:
                messages.error(request,'OUT OF STOCK')
                return redirect('checkout')
        



        if request.method == "POST":
            
            address_id = request.POST.get('selected_address')
            address = Address.objects.get(id = address_id)
            payment_method = request.POST.get('payment_option')
            total_amount = request.POST.get('sub_total')

            if payment_method != 'cod':
                mes = 'choosen payment option currently not avilable...We are working on that'
                messages.error(request,mes)
                return redirect('checkout')
                
            
            if payment_method == 'cod':
                order_id = Order.objects.create(
                    user = user,
                    address = address,
                    total_amount = total_amount,
                    payment_method = payment_method,
                )

                cart_objects = Cart.objects.filter(user_id=user)

                for cart_obj in cart_objects:
                    var = Variant.objects.get(product_id=cart_obj.size_variant.product_id, size=cart_obj.size_variant.size)
                    var.stock = var.stock-cart_obj.quantity 
                    var.save()

                    OrderedProducts.objects.create(
                        order_id = order_id,
                        user = user,
                        product = cart_obj.size_variant,
                        size = cart_obj.size_variant.size,
                        quantity = cart_obj.quantity,
                        total_amount = total_amount,
                        status = 'Order confirmed',
                        address = address
                    )
                
                cart_objects.delete()
                return render(request,'thankyou.html')
            
        
    return redirect('login')



def my_order(request):
    obj = Order.objects.all()
    context = { 'order' : obj }
    return render(request,'my_order.html',context)


def view_order(request,id):
    orders = OrderedProducts.objects.filter(order_id=id)
    address = Order.objects.get(id=id)
    context = { 'orders' : orders,
               'addr' :address }

    return render(request,'order_details.html',context)



def order_history(request):
    obj = OrderedProducts.objects.all()
    for order_product in obj:
        order_product.pro_total = order_product.product.product_id.selling_price * order_product.quantity                
        
    context = { 'order' : obj }
    return render(request,'order_history.html',context)


def order_details(request):
    return render(request,'order_details.html')




def order_cancel(request,id):
    print(id)
    if 'email' in request.session:
        if request.method == 'POST':
            email_id = request.session.get('email')
            user = Customer.objects.get(email = email_id)

            ordered_id = request.POST.get('orderid')
            print(ordered_id)
            
            ord_pro = OrderedProducts.objects.get(id=id)
            print(ord_pro,ord_pro.product.product_id,ord_pro.product.id)
            #change the status
            ord_pro.status = 'Cancelled'
            pro = Variant.objects.get(product_id = ord_pro.product.product_id, id=ord_pro.product.id )
            #re stocking
            pro.stock = pro.stock + ord_pro.quantity
            ord_pro.save()
            pro.save()

            messages.success(request,'product of cancelled')
            return redirect(view_order,id = ordered_id)
        
        messages.error(request,'some issues facing. try again later...')
        return redirect('view_order')

            

            

            
        

       


