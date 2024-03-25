from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from logintohome.models import Customer
from .models import *
from datetime import datetime, timedelta
from manage_order.models import *
from django.utils import timezone
from django.db.models import Sum, Count
from django.core.paginator import Paginator

# Create your views here.


def AdminLogin(request):
    if "email" in request.session:
        return redirect("error_page")

    if request.user.is_authenticated:
        return redirect("AdminHome")

    if request.method == "POST":
        username1 = request.POST.get("username1")
        password = request.POST.get("password")

        admin = authenticate(username=username1, password=password)

        if admin is not None:
            login(request, admin)
            return redirect("AdminHome")
        else:
            messages.error(request, "Username or password is invalid")
            return render(request, "admin_login.html")

    return render(request, "admin_login.html")


@login_required(login_url="adminlogin")
def AdminHome(request):
    if "email" in request.session:
        return redirect("error_page")

    last_orders = OrderedProducts.objects.all().order_by("-id")[:5]
    orders = OrderedProducts.objects.filter(status="Delivered")
    user = Customer.objects.filter(is_verified=True, is_blocked=False)
    orders_count = orders.count()
    user_count = user.count()
    offer_amount = 0
    offer_amount = orders.aggregate(
        total_discount=Sum("order_id__coupon_id__discount_amount")
    )["total_discount"]
    total_amount = orders.aggregate(total=Sum("total_amount"))["total"] or 0
    delivered_orders = Order.objects.filter(orderedproducts__in=orders)
    payment_methods = delivered_orders.values("payment_method").annotate(
        total_orders=Count("id")
    )
    payment_method_labels = [item["payment_method"] for item in payment_methods]
    payment_method_data = [item["total_orders"] for item in payment_methods]

    monthly_sales_data = []
    months_data = [
        ("Jan", 1),
        ("Feb", 2),
        ("Mar", 3),
        ("Apr", 4),
        ("May", 5),
        ("Jun", 6),
        ("Jul", 7),
        ("Aug", 8),
        ("Sep", 9),
        ("Oct", 10),
        ("Nov", 11),
        ("Dec", 12),
    ]

    for month_name, month_number in months_data:
        monthly_sales = (
            orders.filter(order_id__order_date__month=month_number).aggregate(
                sum=Sum("total_amount")
            )["sum"]
            or 0
        )
        monthly_sales_data.append(int(monthly_sales))

    order_status = OrderedProducts.objects.values("status").annotate(
        total_count=Count("status")
    )
    order_status_type = [order["status"] for order in order_status]
    order_status_count = [order["total_count"] for order in order_status]

    top_products = (
        orders.values("product__product_id__name")
        .annotate(total_sales=Count("product"))
        .order_by("-total_sales")[:10]
    )
    top_categories = (
        Category.objects.annotate(
            total_ordered_products=Count("products__variant__product_id__category")
        )
        .order_by("-total_ordered_products")
        .values("name", "total_ordered_products")[:10]
    )

    context = {
        "orders_count": orders_count,
        "total_amount": total_amount,
        "offer_amount": offer_amount,
        "user_count": user_count,
        "payment_methods": payment_methods,
        "top_products": top_products,
        "top_categories": top_categories,
        "last_orders": last_orders,
        "payment_method_labels": payment_method_labels,
        "payment_method_data": payment_method_data,
        "monthly_sales_data": monthly_sales_data,
        "order_status_type": order_status_type,
        "order_status_count": order_status_count,
    }

    return render(request, "admin_home.html", context)


@never_cache
def AdminLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("adminlogin")


@login_required(login_url="adminlogin")
def manage_user(request):
    context = {}
    if "email" in request.session:
        return redirect("error_page")
    data = Customer.objects.all().order_by('id')

    search = request.GET.get('search')
    if search:
        data = Customer.objects.filter(username__istartswith = search)
        context["data"] = data

    if search:
        context['disable_pagination'] = True    
        

    page = 1
    if request.GET:
        page = request.GET.get('page', 1)

    paginator = Paginator(data,5)
    data = paginator.get_page(page)
    context["data"] = data

    context['data'] = data
    return render(request, "user_manage.html", context)


@never_cache
def Blockuser(request, id):
    user = Customer.objects.get(id=id)
    user.is_blocked = True
    user.save()
    return redirect("manageuser")


@never_cache
def Unblockuser(request, id):
    user = Customer.objects.get(id=id)
    user.is_blocked = False
    user.save()
    return redirect("manageuser")


@login_required(login_url="adminlogin")
def product_offers(request):
    context = {}
    if "email" in request.session:
        return redirect("error_page")
    
    offers = Product_Offer.objects.all()
    product = products.objects.all()
    context["products"] = product
    
    search = request.GET.get('search')
    if search:
        offers = Product_Offer.objects.filter(product_id__name = search)
        context["offers"] = offers

    if search:
        context['disable_pagination'] = True    
        

    page = 1
    if request.GET:
        page = request.GET.get('page', 1)

    paginator = Paginator(offers,5)
    offer = paginator.get_page(page)
    context["offers"] = offer
    

    return render(request, "product_offers.html", context)


@login_required(login_url="adminlogin")
def add_product_offers(request):
    if "email" in request.session:
        return redirect("error_page")

    now_date = timezone.now().date()

    if request.method == "POST":
        pro_id = request.POST.get("productName")
        percentage = request.POST.get("percentage")
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        try:
            product = products.objects.get(id=pro_id)

            if not 1 <= float(percentage) < 100:
                messages.error(request, "Percentage must be between 1 and 100.")
                return redirect("product_offers")

            percentage = float(percentage)

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if Product_Offer.objects.filter(product_id=product).exists():
                messages.error(request, f'Offer Already exists with "{product}"')
                return redirect("product_offers")

            if end_date < start_date:
                messages.error(request, "End date must be after start date.")
                return redirect("product_offers")

            if now_date > end_date:
                messages.error(
                    request, "The end date for the Offer cannot be in the past."
                )
                return redirect("product_offers")

            offers = Product_Offer(
                product_id=product,
                percentage=percentage,
                start_date=start_date,
                end_date=end_date,
            )
            offers.save()

            messages.success(request, f"'{product}' added '{percentage}%' offer ")
            return redirect("product_offers")

        except products.DoesNotExist:
            messages.error(request, "Invalid product selected.")

    return redirect("adminlogin")


@login_required(login_url="adminlogin")
def edit_product_offers(request, id):
    if "email" in request.session:
        return redirect("error_page")

    now_date = timezone.now().date()
    offer = Product_Offer.objects.get(id=id)

    if request.method == "POST":
        percentage = request.POST.get("percentage")
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        try:
            offer = Product_Offer.objects.get(id=id)
            if not 0 <= float(percentage) <= 100:
                messages.error(request, "Percentage must be between 0 and 100.")
                return redirect("product_offers")

            percentage = float(percentage)

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if end_date < start_date:
                messages.error(request, "End date must be after start date.")
                return redirect("product_offers")

            if now_date > end_date:
                messages.error(
                    request, "The end date for the Offer cannot be in the past."
                )
                return redirect("product_offers")

            offer.percentage = percentage
            offer.start_date = start_date
            offer.end_date = end_date
            offer.save()

            messages.success(request, f"'{offer}' Updated with '{percentage}%' offer ")
            return redirect("product_offers")

        except products.DoesNotExist:
            messages.error(request, "Invalid product selected.")

    return render(request, "product_offers.html")


@login_required(login_url="adminlogin")
def product_offer_status(request, id):
    status = Product_Offer.objects.get(id=id)

    if status.is_active == True:
        status.is_active = False
        status.save()
        messages.success(request, "Status changed")
        return redirect("product_offers")
    else:
        status.is_active = True
        status.save()
        messages.success(request, "Status changed")
        return redirect("product_offers")


@login_required(login_url="adminlogin")
def category_offers(request):
    if "email" in request.session:
        return redirect("error_page")

    offers = Category_Offer.objects.all()
    category = Category.objects.all()

    context = {"offers": offers, "categories": category}

    return render(request, "category_offers.html", context)


@login_required(login_url="adminlogin")
def add_category_offers(request):
    if "email" in request.session:
        return redirect("error_page")

    if request.method == "POST":
        cat_id = request.POST.get("CategoryName")
        percentage = request.POST.get("percentage")

        try:
            category = Category.objects.get(id=cat_id)

            if Category_Offer.objects.filter(category_id=category).exists():
                messages.error(request, f'Offer already Exists with "{cat_id}"')
                return redirect("category_offers")

            if not 0 <= float(percentage) <= 100:
                messages.error(request, "Percentage must be between 0 and 100.")
                return redirect("product_offers")

            percentage = float(percentage)

            offers = Category_Offer(category_id=category, percentage=percentage)
            offers.save()
            messages.success(request, f"'{category}' added '{percentage}%' offer ")
            return redirect("category_offers")

        except products.DoesNotExist:
            messages.error(request, "Invalid Category selected.")

    return redirect("adminlogin")


@login_required(login_url="adminlogin")
def edit_category_offers(request, id):
    if "email" in request.session:
        return redirect("error_page")

    offer = Category_Offer.objects.get(id=id)
    if request.method == "POST":
        percentage = request.POST.get("percentage")

        if not 0 <= float(percentage) <= 100:
            messages.error(request, "Percentage must be between 0 and 100.")
            return redirect("category_offers")

        percentage = float(percentage)
        offer.percentage = percentage
        offer.save()

        messages.success(request, "Offer Updated")
        return redirect("category_offers")

    return render(request, "category_offers.html")


@login_required(login_url="adminlogin")
def category_offer_status(request, id):
    status = Category_Offer.objects.get(id=id)

    if status.is_active == True:
        status.is_active = False
        status.save()
        messages.success(request, "Status changed")
        return redirect("category_offers")

    else:
        status.is_active = True
        status.save()
        messages.success(request, "Status changed")
        return redirect("category_offers")


@login_required(login_url="adminlogin")
def sales_report(request):
    if "email" in request.session:
        return redirect("error_page")

    orders = None
    if request.method == "POST":
        filter_type = request.POST.get("filter")
        date_of_download = timezone.now()

        if filter_type == "fixed":
            interval = request.POST.get("interval")

            if interval == "day":
                end_date = timezone.now()
                start_date = end_date - timedelta(days=1)
                orders = OrderedProducts.objects.filter(
                    status="Delivered", delivery_date__range=(start_date, end_date)
                )

            if interval == "week":
                end_date = timezone.now()
                start_date = end_date - timedelta(days=7)
                orders = OrderedProducts.objects.filter(
                    status="Delivered", delivery_date__range=(start_date, end_date)
                )

            if interval == "month":
                end_date = timezone.now()
                start_date = end_date - timedelta(days=30)
                orders = OrderedProducts.objects.filter(
                    status="Delivered", delivery_date__range=(start_date, end_date)
                )

            if interval == "year":
                end_date = timezone.now()
                start_date = end_date - timedelta(days=365)
                orders = OrderedProducts.objects.filter(
                    status="Delivered", delivery_date__range=(start_date, end_date)
                )

        if filter_type == "custom":
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            orders = OrderedProducts.objects.filter(
                status="Delivered", delivery_date__range=(start_date, end_date)
            )

    context = {"orders": orders, "date_of_download": date_of_download}

    return render(request, "sales_report.html", context)
