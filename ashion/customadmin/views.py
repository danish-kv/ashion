from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse
from logintohome.models import Customer

# Create your views here.

def AdminLogin(request):
    if 'username1' in request.session:
        return redirect('AdminHome')
    
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password = request.POST.get('password')

        admin = authenticate(username=username1, password=password)

        if admin is not None:
            request.session['username1'] = username1
            return redirect('AdminHome')
        else:
            messages.error(request, 'Username or password is invalid')
            return render(request,'admin_login.html')
        
    return render(request, 'admin_login.html')



def AdminHome(request):
    if 'username1' in request.session:
        return render(request, 'admin_home.html')
    else:
        return render(request,'admin_login.html')



@never_cache
def AdminLogout(request):
    if 'username1' in request.session:
        request.session.flush()

    return redirect('adminlogin')





def manage_user(request):
    if 'username1' in request.session:
        data = Customer.objects.all()
        context = {'data' : data}

        return render(request,'user_manage.html',context)
    return redirect(AdminLogin)


def Blockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = True
    user.save()
    return redirect('manageuser')

def Unblockuser(request,id):
    user = Customer.objects.get(id = id)
    user.is_blocked = False
    user.save()
    return redirect('manageuser')



