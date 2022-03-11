from django.http.response import JsonResponse
from django.shortcuts import render
from django import template
# Create your views here.

#imports propios
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect,render
from grocery_shop.library.db_manager import insert_order_ajax,upload_products_by_excel,insert_order,get_cart,generate_meat_report,update_cart,generate_individual_reports,generate_group_reports
from django.contrib.auth.decorators import login_required
from grocery_shop.models import Category, Product,Unit,Order,Shop
from users.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date,datetime



def out_service(request):
    pass
    return render(request,'grocery_store/out_service.html')



@login_required
def insert_to_cart(request):
    try: 
        order_id = request.GET['id']
        user = request.GET['user']
        ammount = request.GET['ammount']
        user = User.objects.get(username=user)
        product = Product.objects.get(id=int(order_id))
        print("H---------------------------")
        message,unit,product = insert_order_ajax(request,order_id,user,product,ammount)
    
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
        shops = Shop.objects.all()
        return render(request,'grocery_store/cart.html',{"orders":orders,"shops":shops})

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
    print("40 solicitudes")
    print(cont)
    id_shop = request.GET['shop']
    print("***************************************")
    print(id_shop)
    if id_shop=="0":
        print("Son todos")
        products_list = Product.objects.filter(active=True)
    else:
        print("Se busca por tienda")
        products_list = Product.objects.filter(active=True,shop_name=id_shop)
    peg = Paginator(products_list, 4)
    products = peg.page(cont).object_list
    serialized_q = json.dumps(list(products.values()),  ensure_ascii=True)
    return JsonResponse(serialized_q,status=200,safe=False)

@login_required
def get_item(request):
    pass
    id_m=int(request.GET['id'])
    product = Product.objects.filter(id=id_m)
    product2 = Product.objects.get(id=id_m)
    d = list(product.values_list('id','name','price')) 
    b =str(product2.unit_name)
    new_ = d[0] + (b,)
    my_list = []
    my_list.append(new_)
    serialized_q = json.dumps(my_list,  ensure_ascii=True)
    return JsonResponse(serialized_q,status=200,safe=False)


@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('start')
    
@login_required
def menu(request):
    if request.method == 'POST':
        if 'search_bar' in request.POST:
            bsq = request.POST.get('search_bar')
            products_list = Product.objects.filter(name__icontains=bsq)
            shops = Shop.objects.all()
            page = request.GET.get('page', 1)
            peg = Paginator(products_list, 10)
            products = peg.page(page)
            return render(request,'grocery_store/menu.html',{'products_list': products_list,'products': products,'shops':shops,'page':1})
        if 'group_report' in request.POST:
            pass

    else:
        if 'shop' in request.GET:
            id_shop = request.GET['shop']
            products_list = Product.objects.filter(active=True,shop_name=id_shop)
            page = request.GET.get('page', 1)
            shops = Shop.objects.all()
            peg = Paginator(products_list, 4)
            products = peg.page(page)
            return render(request,'grocery_store/menu.html',{"id_shop":id_shop,'products_list': products_list,'page':1,'products': products,'shops':shops})
        
        else:
            id_shop = 0
            products_list = Product.objects.filter(active=True)
            page = request.GET.get('page', 1) 
            shops = Shop.objects.all()
            peg = Paginator(products_list, 4)
            page = request.GET.get('page', 1)
            products = peg.page(page)
            return render(request,'grocery_store/menu.html',{"id_shop":id_shop,'products_list': products_list,'products': products,'shops':shops,'page':page})

def index(request):
    if request.method == 'POST':
        pass
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            if ("Comun" == user.profile_user.area or user.profile_user.area == "Admin") and "Activo" == user.profile_user.active:
                pass
                login(request,user)
                return redirect('menu')
            else:
                return render(request,'grocery_store/index.html',{'error':'No tienes permisos para entrar'})
            
        else:
            return render(request,'grocery_store/index.html',{'error':'Usuario o contraseña invalidos'})
    
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    actual_date  = datetime.now()
    x=actual_date
    print(day[x.weekday()])
    if (current_time>"12:00:00" and day[x.weekday()]=="Tuesday"):
        pass
        print("filtro")
        return redirect('out_service')
    else:
        print("manitas")
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
            return generate_individual_reports(week)
            #return render(request,'grocery_store/store_reports.html')
        if 'group_report' in request.POST:
            pass 
            week = request.POST['group_report']
            week = str(week)
            return generate_group_reports(week)
        if 'meat_report' in request.POST:
            pass 
            week = request.POST['meat_report']
            week = str(week)
            return generate_meat_report(week)
        else:
            return render(request,'grocery_store/store_reports.html')
    else:
        return render(request,'grocery_store/store_reports.html')






    
