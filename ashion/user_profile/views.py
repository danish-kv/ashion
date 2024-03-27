from django.shortcuts import render, redirect
from logintohome.models import Customer
from django.contrib import messages
from .models import *
# Create your views here.


def user_profile(request):
    if "email" in request.session:
        user_id = request.session.get("email")
        user = Customer.objects.get(email=user_id)
        use = user
        address = Address.objects.filter(user=use, is_available=True)
        wallet = Wallet_User.objects.filter(user_id = use).last()

        context = {"user": user,
                   "addresses": address,
                   'wallet' : wallet }

        return render(request, "user_dashbord.html", context)
    return redirect("login")


def update_profile(request):
    if "email" in request.session:
        if request.method == "POST":
            email_id = request.session.get("email")
            name = request.POST.get("name")
            number = request.POST.get("number")
            dob = request.POST.get("dob")
            gender = request.POST.get("gender")

            if name.strip() == "":
                messages.error(request, "Name field is Empty")
                return redirect("user_profile")

            if number.strip() == "":
                messages.error(request, "Number field is Empty")
                return redirect("user_profile")

            if gender.strip() == "":
                messages.error(request, "Name field is Empty")
                return redirect("user_profile")

            user = Customer.objects.get(email=email_id)
            user.username = name
            user.number = number
            user.dob = dob
            user.gender = gender
            user.save()
            messages.success(request, "details update successfully")
            return redirect("user_profile")
        return redirect("user_profile")
    return redirect("login")


def change_password(request):
    if "email" in request.session:
        if request.method == "POST":
            user_id = request.session.get("email")
            old_password = request.POST.get("oldPassword")
            new_password = request.POST.get("newPassword")
            confirm_password = request.POST.get("conPassword")

            try:
                user = Customer.objects.get(email=user_id)
            except:
                messages.error(request, "User is not found")
                return redirect("login")

            if old_password.strip() == "":
                messages.error(request, "Old password field is Empty")
                return redirect("user_profile")

            if new_password.strip() == "":
                messages.error(request, "New password field is Empty")
                return redirect("user_profile")

            if confirm_password.strip() == "":
                messages.error(request, "Confrim password field is Empty")
                return redirect("user_profile")

            if user.password != old_password:
                messages.error(request, "Old Password is incorrect")
                return redirect("user_profile")

            if user.password == new_password:
                messages.error(request, "Old Password and new password are the same")
                return redirect("user_profile")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("user_profile")

            if len(new_password) < 6:
                messages.error(request, "Password should be atleast 6 charaters long")
                return redirect("user_profile")

            user.password = new_password
            user.save()

            messages.success(
                request, "Password changed successfully.  Please login again."
            )
            request.session.clear()
            return redirect("login")

    return redirect("login")


def edit_address(request, id):
    add = Address.objects.get(id=id)
    context = {"edit_address": add}

    if request.method == "POST":
        name = request.POST.get("name")
        number = int(request.POST.get("number"))
        address = request.POST.get("address")
        state = request.POST.get("state")
        district = request.POST.get("district")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        landmark = request.POST.get("landmark")

        if name.strip() == "":
            messages.error(request, "Name field is Empty")
            return redirect("user_profile")

        if str(number).strip() == "":
            messages.error(request, "Number field is Empty")
            return redirect("user_profile")

        if address.strip() == "":
            messages.error(request, "Address field is Empty")
            return redirect("user_profile")

        if state.strip() == "":
            messages.error(request, "State field is Empty")
            return redirect("user_profile")

        if district.strip() == "":
            messages.error(request, "District field is Empty")
            return redirect("user_profile")

        if city.strip() == "":
            messages.error(request, "City field is Empty")
            return redirect("user_profile")

        if landmark.strip() == "":
            messages.error(request, "Landmark field is Empty")
            return redirect("user_profile")

        if len(str(number)) != 10:
            messages.error(request, "Phone Number should be 10 digits")
            return redirect("user_profile")

        add.name = name
        add.number = number
        add.address = address
        add.state = state
        add.district = district
        add.city = city
        add.pincode = pincode
        add.landmark = landmark
        add.save()
        messages.success(request, f"'{name}'s Adderss edited succuessfuly")
        return redirect("user_profile")

    return render(request, "edit_address.html", context)


def delete_address(request, id):
    add = Address.objects.get(id=id)
    add.is_available = False
    add.save()
    messages.success(request, "Address deleted successfully")
    return redirect("user_profile")


def wallet(request):
    if "email" in request.session:
        email = request.session.get("email")
        user = Customer.objects.get(email=email)
        wallet = Wallet_User.objects.filter(user_id=user).order_by("-id")

        if wallet:
            balance = wallet.first().balance
        else:
            balance = 0

        context = {"wallet": wallet, "user": user, "balance": balance}

        return render(request, "wallet.html", context)
    return redirect("login")
