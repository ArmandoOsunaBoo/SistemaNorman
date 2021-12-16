from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

#imports propios
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect,render
from grocery_shop.library.db_manager import upload_products_by_excel
from django.contrib.auth.decorators import login_required
from grocery_shop.models import Product
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder


def detalles(request):
    pass
    id_product=int(request.GET['id'])
    product = Product.objects.get(id=id_product)
    return render(request,'grocery_store/detalles.html',{'product':product})


def ajax(request):
    pass
    print("enviando peticion")
    cont=int(request.GET['page'])
    print("----------------------------------")
    products_list = Product.objects.all().order_by("id_master")
    peg = Paginator(products_list, 4)
    products = peg.page(cont).object_list
    print(products)
    print("@---------------------------------------------------------------------------------")
    print((products[0].name))
    serialized_q = json.dumps(list(products.values()),  ensure_ascii=True)
    print(serialized_q)
    return JsonResponse(serialized_q,status=200,safe=False)


@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('login')
    
@login_required
def menu(request):
    pass
    products_list = Product.objects.all()
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

@login_required
def manage(request):
    pass
    if request.method == 'POST':
        if 'upload_products' in request.FILES:
            pass
            print("se ingreso un excel de productos")
            doc = request.FILES
            excel_file = doc["upload_products"]
            upload_products_by_excel(excel_file)

            return render(request,'grocery_store/manage.html')
        else:
            return render(request,'grocery_store/manage.html')
    else:
        print("Entrada normal")
        return render(request,'grocery_store/manage.html')






    
