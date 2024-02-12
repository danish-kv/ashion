from django.shortcuts import render, redirect
from .models import Brand, Category
from django.contrib import messages





def brand_view(request):
    pass

def add_brand_view(request):
    if request.method == "POST":
        brand_name = request.POST.get('brand_name')

        if Brand.objects.filter(name__contains=brand_name).exists():
            messages.error(request, f'Brand with name "{brand_name}" already exists!')
            return redirect('addbrand')
        
        data  = Brand(name = brand_name)
        data.save()
        messages.success(request,'Brand added. ')

    return render(request, 'add_brand.html')

def edit_brand_view(request):
    pass




def category_view(request):
    if 'username1' in request.session:

        categories = Category.objects.all()
        context = {'category' : categories}
        return render(request, 'category.html',context)
    
    return redirect('adminlogin')


def add_category_view(request):
    if 'username1' in request.session:

        if request.method == "POST":
            category_name = request.POST.get('category_name')

            if Category.objects.filter(name__contains=category_name).exists():
                messages.error(request, f'Category with name "{category_name}" already exists!')
                return redirect('addcategory')
            
            Subdata  = Category(name = category_name)
            Subdata.save()
            messages.success(request,f'{category_name} added ')
            return redirect('category')
        
        return render(request, 'add_category.html')
    
    return redirect('adminlogin')



def edit_category_view(request,id):
    if 'username1' in request.session:
        if request.method == 'POST':
        
            name = request.POST.get('category_name')
            is_listed = request.POST.get('is_listed', False)
            is_listed = request.POST.get('is_listed') == 'on'

            # Check if 'True' is present in the list of values
            
            print(is_listed,name)
            obj = Category.objects.get(id = id)
            obj.name = name
            obj.is_listed = is_listed
            obj.save()
            messages.success(request,f'{name} edited')
            return redirect('category')

        obj1 = Category.objects.get(id = id)
        context = {'category' : obj1 }
        return render(request, 'edit_category.html',context)  
    
    return redirect('adminlogin')



def list_category(request,id):
    if 'username1' in request.session:

        obj = Category.objects.get(id = id)
        obj.is_listed = True
        obj.save()
        return redirect('category')
    return redirect('adminlogin')


def unlist_category(request,id):
    if 'username1' in request.session:

        obj = Category.objects.get(id = id)
        obj.is_listed = False
        obj.save()
        return redirect('category')
    
    return redirect('adminlogin')
