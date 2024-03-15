from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import Cart
from manage_product.models import *
from logintohome.models import Customer
from django.contrib import messages
from user_profile.models import *
from django.views.decorators.cache import never_cache
from .models import Checkout as checkout
from manage_order.models import *
from  manage_product.models import Variant
from manage_order.models import CancelledOrder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
from manage_coupen.models import Coupons
from decimal import Decimal
# Create your views here.



#cart
def showcart(request):
    if 'email' in request.session:
        us_id = request.session.get('email')
        user = Customer.objects.get(email = us_id)

        cart = Cart.objects.filter(user_id = user).order_by('-id')
        sub_total1 = 0
        
        for cart_product in cart:
            discounted_price = cart_product.size_variant.product_id.discounted_price()

            if discounted_price < cart_product.size_variant.product_id.selling_price:
                cart_product.pro_total = discounted_price * cart_product.quantity

            else:
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
        addresses = Address.objects.filter(user = user, is_available=True).order_by('-id')
        cart_items = Cart.objects.filter(user_id = user.id)


        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')
        
            
        
        final_amount = 0
        product_total = 0
        offer_amount = 0

        

        for cart_product in cart_items:
            discounted_price = cart_product.size_variant.product_id.discounted_price()

            if discounted_price < cart_product.size_variant.product_id.selling_price:
                cart_product.pro_total = discounted_price * cart_product.quantity

            else:
                cart_product.pro_total = cart_product.size_variant.product_id.selling_price * cart_product.quantity  
            
            final_amount += cart_product.pro_total
            product_total += cart_product.pro_total
            print(final_amount,product_total)
            print()


            
        try:
            checkout_obj = checkout.objects.get(user_id = user.id)
            checkout_obj.user_id = user.id
            checkout_obj.sub_total = final_amount
            checkout_obj.save()
        except:
            checkout_obj = checkout(user_id = user.id, sub_total = final_amount)
            checkout_obj.save()

        if checkout_obj.coupon_active == True:
            coupon_amount = checkout_obj.coupon.discount_amount    
            print(f'Coupon Amount {coupon_amount}')     

            offer_amount = coupon_amount
            final_amount -= coupon_amount

            print(offer_amount, final_amount)


        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY , settings.RAZORPAY_API_SECRET))
        payment = client.order.create({ 'amount' : float(final_amount) * 100, 'currency' : 'INR', 'payment_capture' : 1 })

        print(payment)

        coupons = Coupons.objects.filter(active = True)

        context = { 'addresses' : addresses,
                   "cart_items" : cart_items,
                   'checkout' : checkout_obj,
                   'final_amount' : final_amount,
                   'payment' : payment,
                   'coupons' : coupons,
                   'product_total' : product_total,
                   'offer_amount' : offer_amount,
                   }
        
        return render(request,'checkout1.html', context)
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
            # if pincode != 6:
            #     messages.error(request,'Pincode should be 6 digits')
            
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



def apply_coupon(request):
    if 'email' in request.session:
        email_id = request.session.get('email')
        user = Customer.objects.get(email=email_id)

        checkout_obj = checkout.objects.get(user=user)

        if request.method == "POST":
            code = request.POST.get('coupon_code')
            print(code)

            
            if checkout_obj.coupon_active:
                return JsonResponse({'error' : 'Coupon already applied'  })

            try:
                coupon_obj = Coupons.objects.get(code__iexact=code.strip())
                print(coupon_obj)
            except Coupons.DoesNotExist:
                return JsonResponse({ 'error' : 'Coupon does not exist' })


            
            if not coupon_obj.active:
                return JsonResponse({'error': 'Coupon is not active'})
            
            current_date = timezone.now().date()
            if coupon_obj.start_date and current_date < coupon_obj.start_date:
                return JsonResponse({'error': 'Coupon is not yet valid'})

            if coupon_obj.end_date and current_date > coupon_obj.end_date:
                return JsonResponse({'error': 'Coupon has expired'})
            
            print(checkout_obj.sub_total)
            print(coupon_obj.min_amount)
            if checkout_obj.sub_total <  coupon_obj.min_amount:

                return JsonResponse({'error': f'Minimum amount requirement not met for this coupon'})
            
            if coupon_obj.quantity is not None and checkout_obj.coupon_active:
                if checkout_obj.coupon.quantity <= 0:
                    return JsonResponse({'error': 'Coupon quantity limit reached'})

            checkout_obj.coupon = coupon_obj
            checkout_obj.coupon_active = True
            checkout_obj.save()
            
            return JsonResponse({'status' : 'Coupon applied'})




def remove_coupen(request,id):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Customer.objects.get(email = email)

        checkout_obj = checkout.objects.get(user=user)

        coupon_id = Coupons.objects.get(id = id)
        if checkout_obj.coupon == coupon_id:
            checkout_obj.coupon = None
            checkout_obj.coupon_active = False
            checkout_obj.save()
            messages.success(request,'Coupon removed')
            return redirect('checkout')
        
        else:
            messages.error(request,'Facing an issue')
            return redirect('checkout')


            
    return redirect('login')




@never_cache
def place_order(request):
    if  'email' in request.session:
        user_id = request.session.get('email')
        user = Customer.objects.get(email = user_id)
        check_out = checkout.objects.get(user = user)

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

                    discounted_price = cart_obj.size_variant.product_id.discounted_price()
                    print(discounted_price)

                    if discounted_price < cart_obj.size_variant.product_id.selling_price:
                        pro_total = discounted_price * cart_obj.quantity
                        print(pro_total)
                    else:
                        pro_total = cart_obj.size_variant.product_id.selling_price * cart_obj.quantity

                    OrderedProducts.objects.create(
                        order_id = order_id,
                        user = user,
                        product = cart_obj.size_variant,
                        size = cart_obj.size_variant.size,
                        quantity = cart_obj.quantity,
                        total_amount = pro_total,
                        status = 'Order confirmed',
                        address = address
                    )
                
                cart_objects.delete()
                check_out.delete()
                return redirect('order_success',order_id.id  )
            
    return redirect('login')



@never_cache
def razorpay_payment(request):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Customer.objects.get(email=email)

        check_out = checkout.objects.get(user = user)

        cart_objects = Cart.objects.filter(user_id=user)

        for cart_obj in cart_objects:
            if cart_obj.quantity > cart_obj.size_variant.stock:
                messages.error(request,'OUT OF STOCK')
                return redirect('checkout')
        
        if request.method == 'POST':
            address_id = request.POST.get('address')
            address = Address.objects.get(id = address_id)
            total_amount = request.POST.get('total_amount')
            payment_method = 'Razor pay'

            
            order_id = Order.objects.create(
                user = user,
                address = address,
                total_amount = total_amount,
                payment_method = payment_method,
                coupon_id = check_out.coupon,
            )

    
            for cart_obj in cart_objects:
                
                var = Variant.objects.get(product_id=cart_obj.size_variant.product_id, size=cart_obj.size_variant.size)
                var.stock = var.stock - cart_obj.quantity 
                var.save()

                discounted_price = cart_obj.size_variant.product_id.discounted_price()

                if discounted_price < cart_obj.size_variant.product_id.selling_price:
                        pro_total = discounted_price * cart_obj.quantity
                        print(pro_total)
                else:
                    pro_total = cart_obj.size_variant.product_id.selling_price * cart_obj.quantity
                
                OrderedProducts.objects.create(
                    order_id = order_id,
                    user = user,
                    product = cart_obj.size_variant,
                    size = cart_obj.size_variant.size,
                    quantity = cart_obj.quantity,
                    total_amount = pro_total,
                    status = 'Order confirmed',
                    address = address
                )

            cart_objects.delete()
            check_out.delete()

            data = {
                'redirect_url' : '/order_success/',
                'order_id' : order_id.id
            }

            return JsonResponse(data)

            
        
    messages.warning(request,'Please login to continue...')
    return redirect('login')








@never_cache
def wallet_payment(request):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Customer.objects.get(email=email)
        check_out = checkout.objects.get(user = user)
        cart_objects = Cart.objects.filter(user_id=user)

        wallet_user = Wallet_User.objects.filter(user_id = user).order_by('-id').first()


        for cart_obj in cart_objects:
            if cart_obj.quantity > cart_obj.size_variant.stock:
                messages.error(request,'OUT OF STOCK')
                return redirect('checkout')
        
        if request.method == 'POST':
            address_id = request.POST.get('address')
            address = Address.objects.get(id = address_id)
            total_amount = float(request.POST.get('total_amount'))
            payment_method = 'Wallet'


            if total_amount > int(wallet_user.balance):
                return JsonResponse({'error': f'Insufficient balance in your wallet. Current wallet balance: {int(wallet_user.balance)}'})


            new_balance = wallet_user.balance - int(total_amount)
            print(wallet_user.balance, total_amount, new_balance)
            Wallet_User.objects.create(
                user_id = user,
                transaction_type = "Debit",
                amount = total_amount,
                balance = new_balance
                )
            
            order_id = Order.objects.create(
                user = user,
                address = address,
                total_amount = total_amount,
                payment_method = payment_method,
                coupon_id = check_out.coupon,
            )



            for cart_obj in cart_objects:
                
                var = Variant.objects.get(product_id=cart_obj.size_variant.product_id, size=cart_obj.size_variant.size)
                var.stock = var.stock - cart_obj.quantity 
                var.save()

                discounted_price = cart_obj.size_variant.product_id.discounted_price()

                if discounted_price < cart_obj.size_variant.product_id.selling_price:
                        pro_total = discounted_price * cart_obj.quantity
                        print(pro_total)
                else:
                    pro_total = cart_obj.size_variant.product_id.selling_price * cart_obj.quantity
                
                OrderedProducts.objects.create(
                    order_id = order_id,
                    user = user,
                    product = cart_obj.size_variant,
                    size = cart_obj.size_variant.size,
                    quantity = cart_obj.quantity,
                    total_amount = pro_total,
                    status = 'Order confirmed',
                    address = address
                )

            cart_objects.delete()
            check_out.delete()

            data = {
            'redirect_url': '/order_success/',
            'order_id': order_id.id 
            }
            return JsonResponse(data)
   
    messages.warning(request,'Please login to continue...')
    return redirect('login')






#All orders
def my_order(request):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Customer.objects.get(email = email)
        
        obj = Order.objects.filter(user = user).order_by('-id')
        context = { 'order' : obj }
        return render(request,'my_order.html',context)
    return redirect('login')


#Ordered Products of order
def ordered_products(request,id):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Customer.objects.get(email = email)

        orders = OrderedProducts.objects.filter(order_id=id,user = user)
        address = Order.objects.get(id=id)
        context = { 'orders' : orders,
                'addr' : address }
        
        return render(request,'ordered_products.html',context)
    return redirect('login')


#Order Success
def order_success(request,id):
    orders = OrderedProducts.objects.filter(order_id=id)
    address = Order.objects.get(id=id)
    context = { 'orders' : orders,
               'addr' : address }

    return render(request,'order_success.html',context)




def order_cancel(request,id):
    if 'email' in request.session:
        if request.method == 'POST':
            email_id = request.session.get('email')
            user = Customer.objects.get(email = email_id)

            ordered_id = request.POST.get('orderid')
            reason = request.POST.get('reason')
            ord_pro = OrderedProducts.objects.get(id=id)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(id)
            print(ord_pro)


            if ord_pro.order_id.payment_method == 'cod':
                ord_pro.status = 'Cancelled'
                ord_pro.save()
                CancelledOrder.objects.create(
                    order_id = ord_pro,
                    user_id = user,
                    cancel_reason = reason,
                )

            
            
            elif ord_pro.order_id.payment_method == 'Razor pay' or ord_pro.order_id.payment_method == 'Wallet':
                
                try:
                    discount_amount = 0
                    if ord_pro.order_id.coupon_id:
                        discount_amount = ord_pro.order_id.coupon_id.discount_amount

                    
                    total_products = ord_pro.order_id.orderedproducts_set.count()
                    refund_amount = discount_amount / total_products
                    print(f'{total_products} total products,, {refund_amount} refund_amount ')

                    # refunding amount
                    amount = ord_pro.total_amount - Decimal(refund_amount)
                    print(amount)
                    print( ord_pro.total_amount)
                    print(ord_pro.quantity)
                    print( refund_amount)
                    wallet_user = Wallet_User.objects.filter(user_id = user).order_by('-id').first()
                    if not wallet_user:
                        balance = 0
                    else:
                        balance = wallet_user.balance
                    new_balance = balance + amount
                    Wallet_User.objects.create(
                        user_id = user,
                        transaction_type = "Credit",
                        amount = amount,
                        balance = new_balance
                    )

                except Exception as e:
                    print(e)
                    messages.error(request,f'Facing some issues {str(e)}')
                    #Change the status and ReStocking
                    
            pro = Variant.objects.get(product_id = ord_pro.product.product_id, id=ord_pro.product.id )
            pro.stock = pro.stock + ord_pro.quantity
            ord_pro.save()
            pro.save()
            ord_pro.status = 'Cancelled'
            ord_pro.save()
            CancelledOrder.objects.create(
                order_id = ord_pro,
                user_id = user,
                cancel_reason = reason,
            )
            messages.success(request,'Product cancelled')
            return redirect('ordered_products',id = ordered_id)
                
                

            
                
        
        messages.error(request,'some issues facing. try again later...')
        return redirect('ordered_products',id = ordered_id)




def return_order(request,id):
    if 'email' in request.session:
        if request.method == 'POST':
            email_id = request.session.get('email')
            user = Customer.objects.get(email = email_id)

            ordered_id = request.POST.get('orderid')
            reason = request.POST.get('reason')
            ord_pro = OrderedProducts.objects.get(id=id)

            try:
                discounted_amount = 0
                if ord_pro.order_id.coupon_id:
                    discounted_amount = ord_pro.order_id.coupon_id.discount_amount

                total_products = ord_pro.order_id.orderedproducts_set.count()
                refund_amount = discounted_amount / total_products
                print(f'{total_products} total products,, {refund_amount} refund_amount ')

                # refunding amount
                for product in ord_pro.order_id.orderedproducts_set.all():
                    amount = product.total_amount - Decimal(refund_amount)
                    print(amount)
                    print( product.total_amount)
                    print(product.quantity)
                    print( refund_amount)
                    wallet_user = Wallet_User.objects.filter(user_id = user).order_by('-id').first()

                    if not wallet_user:
                        balance = 0
                    else:
                        balance = wallet_user.balance

                    new_balance = balance + amount
                    Wallet_User.objects.create(
                        user_id = user,
                        transaction_type = "Credit",
                        amount = amount,
                        balance = new_balance
                    )


                    #Change the status and ReStocking
                    product.status = 'Returned'
                    pro = Variant.objects.get(product_id = ord_pro.product.product_id, id=ord_pro.product.id )
                    pro.stock = pro.stock + ord_pro.quantity
                    product.save()
                    pro.save()



                OrderReturns.objects.create(
                order_id = ord_pro,
                user = user,
                reason = reason)

                messages.success(request,'Product Returned')
                return redirect('ordered_products',id = ordered_id)
            
            except Exception as e:
                print(e)
                messages.error(request,f'Facing some issues {str(e)}')
        
        messages.error(request,'some issues facing. try again later...')
        return redirect('ordered_products',id = ordered_id)

            

            

            
        

       


