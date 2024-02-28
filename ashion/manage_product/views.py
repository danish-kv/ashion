from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import products, Variant
from django.http import HttpResponse
import os
from manage_category.models import Brand, Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here.




@login_required(login_url='adminlogin')
def product(request):
    product = products.objects.all()
    context = {'product': product}
    return render(request,'product.html',context)


@login_required(login_url='adminlogin')
def addproduct(request):

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        print(category_name)
        cat = Category.objects.get(id = category_name )
        print(cat)
        
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        priority = request.POST.get('priority')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        if products.objects.filter(name__contains=name).exists():
            messages.error(request, f'Product with name "{name}" already exists!')
            return render(request,'add_product.html')
        
        data = products(
            name = name,
            description = description,
            category=cat,
            original_price = original_price,
            selling_price = selling_price,
            priority = priority,
            img1 = img1,
            img2  = img2,
            img3 = img3,
            img4 = img4,
        )
        data.save()
        messages.success(request, f'"{name}" is added Successfully')
        return redirect('product')
    category = Category.objects.filter(is_listed = True)
    context = {'categories' : category}


    return render(request,'add_product.html',context)






@login_required(login_url='adminlogin')
def editproduct(request,id):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description')
        category_name = request.POST.get('category')
        cat = Category.objects.get(name = category_name )
            
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        priority = request.POST.get('priority')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        if products.objects.filter(name__contains=name).exists():
            messages.error(request, f'Product with name "{name}" already exists!')
            return render(request,'edit_product.html')
        obj = products.objects.get(id=id)
        obj.name = name
        obj.description = desc
        obj.category = cat    
        obj.original_price = original_price
        obj.selling_price = selling_price
        obj.priority = priority
        if img1:
            if obj.img1:
                os.remove(obj.img1.path)
            obj.img1 = img1
        if img2:
            if obj.img2:
                os.remove(obj.img2.path)
            obj.img2 = img2
        if img3:
            if obj.img3:
                os.remove(obj.img3.path)
            obj.img3 = img3
        if img4:
            if obj.img4:
                os.remove(obj.img4.path)
            obj.img4 = img4
        obj.save()
        
        
        messages.success(request, 'Product details updated')
        return redirect('product')
    
    product = products.objects.get(id = id)
    category_data = Category.objects.all()
    context = {'product' : product,
            'all_categories' :category_data}
    return render(request,'edit_product.html',context)



@login_required(login_url='adminlogin')
@never_cache
def list_product(request,id):

    obj = products.objects.get(id = id)
    obj.is_listed = True
    obj.save()
    return redirect('product')



@login_required(login_url='adminlogin')
@never_cache
def unlist_product(request,id):

    obj = products.objects.get(id = id)
    print(obj)
    obj.is_listed = False
    obj.save()
    return redirect ('product')




@login_required(login_url='adminlogin')
def Show_variant(request,id):
    var_obj = Variant.objects.filter(product_id = id)
    print(var_obj)
    
    context = {'variants' : var_obj,
               "id" :id,}
    return render(request,'variant.html',context)



@login_required(login_url='adminlogin')
def Add_variant(request,id):

    pro = products.objects.get(id=id)
    context = {'product' : pro}

    if request.method == 'POST':
        pro_id = products.objects.get(id = id)
        size = request.POST.get('size')
        stock = request.POST.get('stock')

        if Variant.objects.filter(size__contains=size, product_id = pro_id).exists():
                messages.error(request, f'Variant of product "{pro_id}" already exists!')
                return render(request,'add_variant.html',context)
        
        Var = Variant(
            product_id = pro_id,
            size = size,
            stock = stock,
        )
        Var.save()
        messages.success(request,f'Variant added for "{pro_id}"')
        return redirect('show_variant',id=id)

    return render(request,'add_variant.html',context)


@login_required(login_url='adminlogin')
def Edit_variant(request,id):
    var = Variant.objects.get(id = id)
    context = {'variant' : var,
               }

    if request.method == "POST": 
        stock = request.POST.get('stock')

        if int(stock) < 0:
            messages.error(request,'Enter Positive number')
            return render(request,'edit_variant.html',context)
        
        obj = Variant.objects.get(id = id)
        obj.stock = stock
        obj.save()
        print(var.product_id.id)
        messages.success(request, f'stock of "{var.product_id}" edited successfully')
        return redirect('show_variant', id=var.product_id.id )


    return render(request,'edit_variant.html',context)

