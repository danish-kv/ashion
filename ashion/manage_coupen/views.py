from django.shortcuts import render, redirect
from .models import Coupons
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

# Create your views here.


@login_required(login_url="adminlogin")
def show_coupon(request):
    if "email" in request.session:
        return redirect("error_page")

    data = Coupons.objects.all()
    context = {"coupons": data}
    return render(request, "coupon.html", context)


@login_required(login_url="adminlogin")
def add_coupon(request):
    if "email" in request.session:
        return redirect("error_page")

    now_date = timezone.now().date()

    if request.method == "POST":
        title = request.POST.get("title")
        code = request.POST.get("code")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        quantity = request.POST.get("quantity")
        min_amount = request.POST.get("min_amount")
        discount_amount = request.POST.get("discount_amount")
        active_check = request.POST.get("active")

        if active_check == "1":
            active = True
        else:
            active = False

        if title.strip() == "":
            messages.error(request, "Please enter Your Coupon title")
            return redirect(add_coupon)

        if code.strip() == "":
            messages.error(request, "Please enter your Coupon code")
            return redirect(add_coupon)

        if end_date < start_date:
            messages.error(request, "End date must be after start date.")
            return redirect(add_coupon)

        if now_date > end_date:
            messages.error(
                request, "The end date for the coupon cannot be in the past."
            )
            return redirect(add_coupon)

        if quantity.strip() == "":
            messages.error(request, "Please enter your Quantity")
            return redirect(add_coupon)

        if min_amount.strip() == "":
            messages.error(request, "Please enter your Minimum Amount")
            return redirect(add_coupon)

        if discount_amount.strip() == "":
            messages.error(request, "Please enter your Discount Amount")
            return redirect(add_coupon)

        if now_date > end_date:
            messages.error(request, "select a proper ending date")
            return redirect(add_coupon)

        obj = Coupons(
            title=title,
            code=code,
            discount_amount=discount_amount,
            start_date=start_date,
            end_date=end_date,
            quantity=quantity,
            min_amount=min_amount,
            active=active,
        )
        obj.save()
        messages.success(request, f'Coupon "{title}" added successfuly')
        return redirect("coupon")

    return render(request, "add_coupon.html")


def edit_coupon(request, id):
    if "email" in request.session:
        return redirect("error_page")

    obj = Coupons.objects.get(id=id)
    context = {"coupon": obj}
    now_date = timezone.now().date()

    if request.method == "POST":
        title = request.POST.get("title")
        code = request.POST.get("code")
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        quantity = request.POST.get("quantity")
        min_amount = request.POST.get("min_amount")
        discount_amount = request.POST.get("discount_amount")
        active_check = request.POST.get("active")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if title.strip() == "":
            messages.error(request, "Please enter a title for your coupon.")
            return redirect(edit_coupon, id)

        if code.strip() == "":
            messages.error(request, "Please enter a code for your coupon.")
            return redirect(edit_coupon, id)

        if end_date < start_date:
            messages.error(request, "End date must be after start date.")
            return redirect(edit_coupon, id)

        if now_date > end_date:
            messages.error(
                request, "The end date for the coupon cannot be in the past."
            )
            return redirect(edit_coupon, id)

        if quantity.strip() == "":
            messages.error(request, "Please enter the quantity of coupons.")
            return redirect(edit_coupon, id)

        if min_amount.strip() == "":
            messages.error(
                request, "Please enter the minimum amount required for this coupon."
            )
            return redirect(edit_coupon, id)

        if discount_amount.strip() == "":
            messages.error(request, "Please enter the discount amount for this coupon.")
            return redirect(edit_coupon, id)

        if active_check == "1":
            active = True
        else:
            active = False

        obj.title = title
        obj.code = code
        obj.discount_amount = discount_amount
        obj.start_date = start_date
        obj.end_date = end_date
        obj.quantity = quantity
        obj.min_amount = min_amount
        obj.active = active
        obj.save()
        messages.success(request, f'Coupon "{title}" is edited succssfully')

        return redirect("coupon")
    return render(request, "edit_coupon.html", context)


def active_coupon(request, id):
    coupon = Coupons.objects.get(id=id)

    if coupon.active == True:
        coupon.active = False
        coupon.save()
    else:
        coupon.active = True
        coupon.save()

    messages.success(request, "Status Changed succssufully")
    return redirect("coupon")
