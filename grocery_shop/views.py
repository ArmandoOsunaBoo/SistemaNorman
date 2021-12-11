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

def ajax(request):
    pass
    print("enviando peticion")
    return JsonResponse({"instancia":"hehe"},status=200)


@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('login')
    
@login_required
def menu(request):
    pass
    products = Product.objects.filter()
    return render(request,'grocery_store/menu.html')

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






    
