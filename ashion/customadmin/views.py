from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from logintohome.models import Customer

# Create your views here.

def AdminLogin(request):
    if request.user.is_authenticated:
        return redirect('AdminHome')

    
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password = request.POST.get('password')

        admin = authenticate(username=username1, password=password)

        if admin is not None:
            login(request, admin)  
            return redirect('AdminHome')
        else:
            messages.error(request, 'Username or password is invalid')
            return render(request,'admin_login.html')
        
    return render(request, 'admin_login.html')



@login_required(login_url='adminlogin')
def AdminHome(request):
    return render(request, 'admin_home.html')




@never_cache
def AdminLogout(request):
    logout(request)  
    return redirect('adminlogin')




@login_required(login_url='adminlogin')  
def manage_user(request):
    data = Customer.objects.all()
    context = {'data' : data}
    return render(request,'user_manage.html',context)




@never_cache 
def Blockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = True
    user.save()
    return redirect('manageuser')




@never_cache
def Unblockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = False
    user.save()
    return redirect('manageuser')



