from django.shortcuts import render, redirect
from .models import Coupons
from django.contrib import messages



# Create your views here.


def show_coupon(request):
    data = Coupons.objects.all()
    context = { 'coupons' : data }
    return render(request,'coupon.html',context)



def add_coupon(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        code = request.POST.get('code')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = request.POST.get('quantity')
        min_amount = request.POST.get('min_amount')
        discount_amount = request.POST.get('discount_amount')
        active_check = request.POST.get('active')

        if active_check == '1':
            active = True
        else:
            active = False

        
        obj = Coupons(
            title = title,
            code = code,
            discount_amount = discount_amount,
            start_date = start_date,
            end_date = end_date,
            quantity = quantity,
            min_amount = min_amount,
            active = active

        )
        obj.save()
        messages.success(request,f'Coupon "{title}" added successfuly')
        return redirect('coupon')

    return render(request,'add_coupon.html')





def edit_coupon(request,id):

    obj = Coupons.objects.get(id = id )
    context = { 'coupon' : obj }

    if request.method == 'POST':
        title = request.POST.get('title')
        code = request.POST.get('code')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = request.POST.get('quantity')
        min_amount = request.POST.get('min_amount')
        discount_amount = request.POST.get('discount_amount')
        active_check = request.POST.get('active')


        if active_check == '1':
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
        messages.success(request,f'Coupon "{title}" is edited succssfully')
        return redirect('coupon')

    return render(request,'edit_coupon.html',context)



def active_coupon(request,id):

    coupon = Coupons.objects.get(id = id)

    if coupon.active == True:
        coupon.active = False
        coupon.save()
    else:
        coupon.active = True
        coupon.save()

    messages.success(request,'Status Changed succssufully')
    return redirect('coupon')
