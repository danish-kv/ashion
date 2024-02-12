from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q

# Create your views here.


def AdminLogin(request):
    if 'username1' in request.session:
        return redirect(AdminHome)
    
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password = request.POST.get('password')

        admin = authenticate(username=username1,password=password)

        if admin is not None:
            request.session['username1']=username1
            return redirect(AdminHome)
        
        else:
            messages.error(request,'Username or password is invalid')
            # return redirect(AdminHome)
        
    return render(request,'admin_login.html')



def AdminHome(request):
    if 'username1' in request.session:
        return redirect(AdminHome)

    return render(request,'admin_home.html')


