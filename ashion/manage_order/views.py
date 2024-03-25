from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from manage_product.models import Variant
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from user_profile.models import Wallet_User
from decimal import Decimal
from django.core.paginator import Paginator
# Create your views here.


@login_required(login_url="adminlogin")
def manage_order(request):
    context = {}
    if "email" in request.session:
        return redirect("error_page")

    orders = (
        OrderedProducts.objects.all()
        .exclude(Q(status="Cancelled") | Q(status="Returned"))
        .order_by("-id")
    )

    search = request.GET.get('search')

    if search:
        orders = OrderedProducts.objects.filter(product__product_id__name__istartswith=search)
        context['order'] = orders


    if search:
        context["disable_pagination"] = True
    

    page = 1
    if request.GET:
        page = request.GET.get('page',1)

    paginator = Paginator(orders,10)
    page_orders = paginator.get_page(page)
    context['order'] = page_orders
    
    return render(request, "admin_order.html", context)


@login_required(login_url="adminlogin")
def order_details_view(request, id):
    if "email" in request.session:
        return redirect("error_page")

    orders = OrderedProducts.objects.get(id=id)
    context = {"obj": orders}
    return render(request, "admin_order_details.html", context)


@login_required(login_url="adminlogin")
def change_order_status(request, id):
    try:
        obj = OrderedProducts.objects.get(id=id)
    except:
        obj = None

    if request.method == "POST":
        try:
            order_status = request.POST.get("statusRadio")
            obj.status = order_status

        except:
            order_status = None

        if order_status == "Delivered":
            obj.delivery_date = timezone.now().date()

        if order_status == "Cancelled":
            if obj.order_id.payment_method == "cod":
                CancelledOrder.objects.create(
                    order_id=obj, user_id=obj.user.id, cancel_reason="Admin Cancelled"
                )
            elif (
                obj.order_id.payment_method == "Razor pay"
                or obj.order_id.payment_method == "Wallet"
            ):
                try:
                    discount_amount = 0
                    if obj.order_id.coupon_id:
                        discount_amount = obj.order_id.coupon_id.discount_amount

                    total_products = obj.order_id.orderedproducts_set.count()
                    refund_amount = discount_amount / total_products

                    # refunding amount
                    amount = obj.total_amount - Decimal(refund_amount)
                    wallet_user = (
                        Wallet_User.objects.filter(user_id=obj.user)
                        .order_by("-id")
                        .first()
                    )
                    if not wallet_user:
                        balance = 0
                    else:
                        balance = wallet_user.balance
                    new_balance = balance + amount
                    Wallet_User.objects.create(
                        user_id=obj.user,
                        transaction_type="Credit",
                        amount=amount,
                        balance=new_balance,
                    )

                except Exception as e:
                    messages.error(request, f"Facing some issues {str(e)}")
                pro = Variant.objects.get(
                    product_id=obj.product.product_id, id=obj.product.id
                )
                pro.stock = pro.stock + obj.quantity
                obj.save()
                pro.save()
                obj.status = "Cancelled"
                obj.save()
                CancelledOrder.objects.create(
                    order_id=obj, user_id=obj.user, cancel_reason="Admin Cancelled"
                )

        messages.success(request, f"Order status changed to {order_status}")
        return redirect("order_deatils_view", id)


@login_required(login_url="adminlogin")
def cancelled_orders(request):
    context = {}
    if "email" in request.session:
        return redirect("error_page")

    datas = CancelledOrder.objects.all()

    search = request.GET.get('search')
    if search:
        datas = CancelledOrder.objects.filter(order_id__product__product_id__name__istartswith=search)
        context['data'] = datas

    if search:
        context["disable_pagination"] = True

    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    
    paginator = Paginator(datas, 9)
    data = paginator.get_page(page)

    context['data'] = data
    return render(request, "cancel_request.html", context)


@login_required(login_url="adminlogin")
def order_return(request):
    context = {}
    if "email" in request.session:
        return redirect("error_page")

    datas = OrderReturns.objects.all()

    search = request.GET.get('search')

    if search:
        datas = OrderReturns.objects.filter(order_id__product__product_id__name__istartswith=search)
        context['data'] = datas

    if search:
        context["disable_pagination"] = True

    page = 1
    if request.GET:
        page = request.GET.get('page', 1)
    
    paginator = Paginator(datas, 9)
    data = paginator.get_page(page)

    context['data'] = data
    return render(request, "order_return.html", context)
