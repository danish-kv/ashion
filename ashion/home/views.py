from django.shortcuts import render, redirect
from django.contrib import messages
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
    context = {}
    product_list = products.objects.filter(is_listed=True)
    pro_offer = Product_Offer.objects.filter(is_active=True)

    data = request.GET.get("data")

    if data == "Women":
        product_list = product_list.filter(category__name=data, is_listed=True)

        context["data"] = "Women"
    elif data == "Men":
        product_list = product_list.filter(category__name=data, is_listed=True)
        context["data"] = "Men"

    elif data == "Kids":
        product_list = product_list.filter(category__name=data, is_listed=True)
        context["data"] = "Kids"

    else:
        context["data"] = "Men"

    search_query = request.GET.get("search")

    if search_query:
        product_list = product_list.filter(name__istartswith=search_query)
        context["product"] = product_list

    # minprice = request.GET.get('minprice')
    # maxprice = request.GET.get('maxprice')
    # if minprice and maxprice:
    #     product_list = product_list.filter(selling_price__gte=minprice, selling_price__lte=maxprice)
    #     context["minprice"] = minprice
    #     context["maxprice"] = maxprice


    sort_by = request.GET.get("sortby")

    if sort_by:
        product_list = product_list.order_by(sort_by)
        context["product_list"] = product_list

    if sort_by or search_query:
        context["disable_pagination"] = True

    page = 1
    if request.GET:
        page = request.GET.get("page", 1)

    paginator = Paginator(product_list, 9)
    product_list = paginator.get_page(page)

    context["product"] = product_list
    return render(request, "product_list.html", context)


def product_details(request, id):
    product = products.objects.get(id=id)
    variants = Variant.objects.filter(product_id=id)
    var = Variant.objects.filter(product_id=id).aggregate(m=Max("stock"))["m"]
    category = Category.objects.filter(is_listed=True)

    related_products = products.objects.filter(category=product.category).exclude(id=product.id)[:4]
    

    context = {
        "product": product,
        "variants": variants,
        "var": var,
        "cat": category,
        'related_products' : related_products
    }
    return render(request, "product_details.html", context)



def add_to_wishlist(request, id, from_page):
    if "email" in request.session:
        email_id = request.session.get("email")

        try:
            user_id = Customer.objects.get(email=email_id)
            product_id = products.objects.get(id=id)

            if Wishlist.objects.filter(product_id=product_id).exists():
                messages.warning(request, "Product is already in your wishlist")
            else:
                Wishlist.objects.create(
                    user_id=user_id,
                    product_id=product_id,
                )
                messages.success(request, "Added to wishlist")

        except Customer.DoesNotExist:
            messages.error(request, "Customer not found")
        except products.DoesNotExist:
            messages.error(request, "Product not found")

        if from_page == "product_details":
            return redirect("productdetails", id=id)
        elif from_page == "home":
            return redirect("home")
        elif from_page == "product_list":
            data = request.GET.get("data")
            if data:
                return redirect(reverse("productlist") + f"?data={data}")
            else:
                return redirect("productlist")

        else:
            return redirect("home")
    else:
        messages.error(request, "Please login for wishlisting a product")
        return redirect("login")


def wishlist(request):
    if "email" in request.session:
        email_id = request.session.get("email")
        user = Customer.objects.get(email=email_id)
        wish = Wishlist.objects.filter(user_id=user)
        context = {"wishlist": wish}
        return render(request, "wishlist.html", context)

    messages.error(request, "Please login first")
    return redirect("login")


def remove_from_wishlist(request, id):
    wish = Wishlist.objects.get(id=id)
    wish.delete()
    messages.success(request, f"'{wish.product_id.name}' removed from wishlist")
    return redirect("wishlist")


def error_page(request):
    return render(request, "errorpage.html")

def soon_page(request):
    return render(request,'coming-soon.html')
