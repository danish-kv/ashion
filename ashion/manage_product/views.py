from django.shortcuts import render ,redirect,  get_object_or_404
from django.contrib import messages
from .models import products
from django.http import HttpResponse
import os
from manage_category.models import Brand, Category
# Create your views here.


def product(request):

    product = products.objects.all()
    context = {'product': product}
    return render(request,'product.html',context)

def addproduct(request):
    if 'username1' in request.session:
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get('description')
            gender = request.POST.get('gender')
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
                gender = gender,
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

        category = Category.objects.all()
        context = {'categories' : category}


        return render(request,'add_product.html',context)
    return redirect('adminlogin')






def editproduct(request,id):
    # obj = products.objects.select_related("category").get(id=id)
    
    if 'username1' in request.session:
        
        if request.method == 'POST':
            name = request.POST.get('name')
            desc = request.POST.get('description')
            category_name = request.POST.get('category')
            cat = Category.objects.get(name = category_name )
                
            gender = request.POST.get('gender')
            original_price = request.POST.get('original_price')
            selling_price = request.POST.get('selling_price')
            priority = request.POST.get('priority')
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            img3 = request.FILES.get('img3')
            img4 = request.FILES.get('img4')

            # if products.objects.filter(name__contains=name).exists():
            #     messages.error(request, f'Product with name "{name}" already exists!')
            #     return render(request,'edit_product.html')

            obj = products.objects.get(id=id)
            obj.name = name
            obj.description = desc
            obj.category = cat    
            obj.gender = gender
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
    return redirect('adminlogin')




def list_product(request,id):
    if 'username1' in request.session:
        obj = products.objects.get(id = id)

        obj.is_listed = True
        obj.save()
        return redirect('product')
    return redirect('adminlogin')

def unlist_product(request,id):
    if 'username1' in request.session:
        obj = products.objects.get(id = id)
        print(obj)
        obj.is_listed = False
        obj.save()
        return redirect ('product')
    return redirect('adminlogin')


