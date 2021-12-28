from django.http.response import JsonResponse
from django.shortcuts import render
from django import template
# Create your views here.

#imports propios
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect,render
from grocery_shop.library.db_manager import upload_products_by_excel,insert_order,get_cart,update_cart,generate_reports
from django.contrib.auth.decorators import login_required
from grocery_shop.models import Product,Unit,Order
from users.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
import datetime




@login_required
def delete_cart_item(request):
    order_id = request.GET['id']
    try:
        Order.objects.filter(id=int(order_id)).delete()
        response = {
            'status': 'True',
            'message': 'Carrito Actualizado con Exito'
        }
        return JsonResponse(response,status=200,safe=False)
    except Exception as e:
        response = {
            'status': 'False',
            'message': 'Hubo un Error al actualizar el carrito'
        }
        print(e)
        return JsonResponse(response,status=200,safe=False)
        
@login_required
def save_cart_items(request):
    amount= request.GET['ammount']
    price= request.GET['price']
    product_name=request.GET['product_name']
    user_name=request.GET['user_names']
    user_id=request.GET['user_id']
    product_ref_id=request.GET['product_ref']
    order_id=request.GET['order_id']
    unit=request.GET['product_unit']
    today = date.today()
    actual_date = today.strftime("%Y-%m-%d")
    try:
        order = Order.objects.get(id=int(order_id))
        print(order.product_name)
        order.date = actual_date
        order.amount = amount
        order.product_name=product_name
        order.user_name=user_name
        order.id_user= User.objects.get(id=int(user_id))
        order.unidad_cantidad=unit
        order.unit=unit
        order.unit_price=price
        order.product_ref =  Product.objects.get(id=int(product_ref_id))
        order.save()
        response = {
            'status': 'True',
            'message': 'Carrito Actualizado con Exito'
        }
        return JsonResponse(response,status=200,safe=False)
    
    except Exception as e:
        response = {
            'status': 'False',
            'message': 'Hubo un Error al actualizar el carrito'
        }
        print(e)
        return JsonResponse(response,status=200,safe=False)
        
    


@login_required
def cart(request):
    pass
    if request.method == 'POST':
        pass
    else:
        orders = get_cart(request.user.id)
        return render(request,'grocery_store/cart.html',{"orders":orders})

@login_required
def detalles(request):
    pass
    if request.method == 'POST':
        pass
        #We attempt to create an order of a caertain product
        message,unit,product = insert_order(request)
        return render(request,'grocery_store/detail.html',{'product':product,"unit":unit,"message":message})
    else:
        #We attempt to get all data from database and iterate them by django-paginator, then iterate with AJAX
        id_product=int(request.GET['id'])
        product = Product.objects.get(id=id_product) 
        unit= Unit.objects.get(id=product.unit_name_id)
    return render(request,'grocery_store/detail.html',{'product':product,"unit":unit})

@login_required
def ajax(request):
    cont=int(request.GET['page'])
    products_list = Product.objects.all().order_by("id_master")
    peg = Paginator(products_list, 4)
    products = peg.page(cont).object_list
    serialized_q = json.dumps(list(products.values()),  ensure_ascii=True)
    return JsonResponse(serialized_q,status=200,safe=False)


@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('start')
    
@login_required
def menu(request):
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    if request.method == 'POST':
        bsq = request.POST.get('search_bar')
        products_list = Product.objects.filter(name__icontains=bsq)
        page = request.GET.get('page', 1)
        peg = Paginator(products_list, 4)
        products = peg.page(page)
        return render(request,'grocery_store/menu.html',{'products_list': products_list,'products': products})

    else:
        products_list = Product.objects.filter(active=True)
        page = request.GET.get('page', 1) 
        print(page)
        peg = Paginator(products_list, 4)
        products = peg.page(page)
        return render(request,'grocery_store/menu.html',{'products_list': products_list,'products': products})

def index(request):
    if request.method == 'POST':
        print("lol")
        pass
        username = request.POST['username']
        password = request.POST['password']
        print(username,':',password)
        user = authenticate(request,username=username,password=password)
        if user:
            if "Comun" == user.profile_user.area and "Activo" == user.profile_user.active:
                pass
                print("eso tiliin")
                login(request,user)
                return redirect('menu')
            else:
                print("weyy nooooo")
                return render(request,'grocery_store/index.html',{'error':'No tienes permisos para entrar'})
            
        else:
            print("neeembre")
            return render(request,'grocery_store/index.html',{'error':'Usuario o contraseña invalidos'})
    
    return render(request,'grocery_store/index.html')




##SECCION DE LA PARTE ADMINISTRATIVA
@login_required
def manage(request):
    pass
    if request.method == 'POST':
        if 'upload_products' in request.FILES:
            pass
            doc = request.FILES
            excel_file = doc["upload_products"]
            upload_products_by_excel(excel_file)
            return render(request,'grocery_store/manage.html')
        else:
            return render(request,'grocery_store/manage.html')
    else:
        return render(request,'grocery_store/manage.html')








@login_required
def reports(request):
    pass
    if request.method == 'POST':
        if 'individual_report' in request.POST:
            pass 
            week = request.POST['individual_report']
            week = str(week)
            generate_reports(week)
            return render(request,'grocery_store/store_reports.html')
        else:
            return render(request,'grocery_store/store_reports.html')
    else:
        return render(request,'grocery_store/store_reports.html')






    
