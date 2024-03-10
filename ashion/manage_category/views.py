from django.shortcuts import render, redirect
from .models import Brand, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache





@login_required(login_url='adminlogin')
def category_view(request):

    categories = Category.objects.all()
    context = {'category' : categories}
    return render(request, 'category.html',context)
    




@login_required(login_url='adminlogin')
def add_category_view(request):

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        is_listed = request.POST.get('is_listed') == 'on'
        if Category.objects.filter(name__contains=category_name).exists():
            messages.error(request, f'Category with name "{category_name}" already exists!')
            return redirect('addcategory')
        
        Subdata  = Category(name = category_name, is_listed=is_listed)
        Subdata.save()
        messages.success(request,f'{category_name} added ')
        return redirect('category')
    
    return render(request, 'add_category.html')


@login_required(login_url='adminlogin')
def edit_category_view(request,id):
    if request.method == 'POST':
    
        name = request.POST.get('category_name')
        is_listed = request.POST.get('is_listed') == 'on'
        
        obj = Category.objects.get(id = id)
        obj.name = name
        obj.is_listed = is_listed
        obj.save()
        messages.success(request,f'{name} edited')
        return redirect('category')
    obj1 = Category.objects.get(id = id)
    context = {'category' : obj1 }
    return render(request, 'edit_category.html',context)  
    


@login_required(login_url='adminlogin')
@never_cache
def list_category(request,id):
    obj = Category.objects.get(id = id)
    obj.is_listed = True
    obj.save()
    return redirect('category')


@login_required(login_url='adminlogin')
@never_cache
def unlist_category(request,id):

    obj = Category.objects.get(id = id)
    obj.is_listed = False
    obj.save()
    return redirect('category')
    
