from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import products, Variant
from django.http import HttpResponse
import os
from manage_category.models import Brand, Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
# Create your views here.




@login_required(login_url='adminlogin')
def product(request):
    if 'email' in request.session:
        return redirect('error_page')
    
    product = products.objects.all()
    context = {'product': product}
    return render(request,'product.html',context)


@login_required(login_url='adminlogin')
def addproduct(request):
    if 'email' in request.session:
        return redirect('error_page')
    
    category = Category.objects.filter(is_listed = True)
    context = {'categories' : category}

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        if Category.objects.filter(id = category_name ).exists():
            cat = Category.objects.get(id = category_name )
        else:
            messages.error(request,'Please select category')
        
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        priority = request.POST.get('priority')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        if name.strip() == "":
            messages.error(request,'Please enter Product name')
            return redirect(addproduct)
        
        if description.strip() == "":
            messages.error(request,'Please enter Product description')
            return redirect(addproduct)
        
        if category_name.strip() == "":
            messages.error(request,'Please Select Category for product')
            return redirect(addproduct)
        
        if float(original_price) < 0:
            messages.error(request,'Not a Valid Amount')
            return redirect(addproduct)
        
        if float(selling_price) < 0:
            messages.error(request,'Not a Valid Amount')
            return redirect(addproduct)
        


        
        if products.objects.filter(name__contains=name).exists():
            messages.error(request, f'Product with name "{name}" already exists!')
            return render(request,'add_product.html')
        
        def is_image(file):
            try:
                img = Image.open(file)
                img.verify()
                get_image_dimensions(file)
                return True
            except Exception as e:
                return False

        if any(file and not is_image(file) for file in [img1, img2, img3, img4]):
            messages.error(request, 'Please upload valid image files.')
            return render(request, 'add_product.html', context)
               
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

    return render(request,'add_product.html',context)



@login_required(login_url='adminlogin')
def editproduct(request,id):
    if 'email' in request.session:
        return redirect('error_page')
    
    product = products.objects.get(id = id)
    category_data = Category.objects.all()
    context = {'product' : product,
            'all_categories' :category_data}
    
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description')
        category_name = request.POST.get('category')
        try :
            cat = Category.objects.get(name = category_name )
        except:
            cat = None
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        priority = request.POST.get('priority')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        if name.strip() == "":
            messages.error(request,'Please enter Product name')
            return redirect(addproduct)
        
        if desc.strip() == "":
            messages.error(request,'Please enter Product description')
            return redirect(addproduct)
        
        if category_name.strip() == "":
            messages.error(request,'Please Select Category for product')
            return redirect(addproduct)
        
        if float(original_price) < 0:
            messages.error(request,'Not a Valid Amount')
            return redirect(addproduct)
        
        if float(selling_price) < 0:
            messages.error(request,'Not a Valid Amount')
            return redirect(addproduct)
        
        if products.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, f'Product with name "{name}" already exists!')
            return render(request,'edit_product.html',context)
        
        def is_image(file):
            try:
                img = Image.open(file)
                img.verify()
                get_image_dimensions(file)
                return True
            except Exception as e:
                return False

        if any(file and not is_image(file) for file in [img1, img2, img3, img4]):
            messages.error(request, 'Please upload valid image files.')
            return render(request, 'edit_product.html', context)
        
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
    if 'email' in request.session:
        return redirect('error_page')

    var_obj = Variant.objects.filter(product_id = id)
    print(var_obj)
    
    context = {'variants' : var_obj,
               "id" :id,}
    return render(request,'variant.html',context)



@login_required(login_url='adminlogin')
def Add_variant(request,id):
    if 'email' in request.session:
        return redirect('error_page')


    pro = products.objects.get(id=id)
    context = {'product' : pro}

    if request.method == 'POST':
        pro_id = products.objects.get(id = id)
        size = request.POST.get('size')
        stock = request.POST.get('stock')

        if float(stock) < 0:
            messages.error(request,'Stock must be greater than 0')
            return render(request,'add_variant.html',context)

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
    if 'email' in request.session:
        return redirect('error_page')

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



