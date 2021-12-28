from django.shortcuts import render


#imports propios
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect,render

from django.contrib.auth.decorators import login_required

def home(request):
    pass
    return render(request,'home.html')

def login_view(request):
    print('ksksksk')
    if request.method == 'POST':
        pass
        username = request.POST['username']
        password = request.POST['password']
        print(username,':',password)
        user = authenticate(request,username=username,password=password)
        if user:
            if "Comun" != user.profile_user.area and "Activo" == user.profile_user.active:
                login(request,user)
                return redirect('dashboard')
            else:
                return render(request,'users/login.html',{'error':'No tienes permisos para entrar'})
        else:
            return render(request,'users/login.html',{'error':'Usuario y contraseña erroneos'})
    return render(request,'users/login.html')

@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('start')


@login_required
def dashboard_view(request):
    pass
    return render(request,'dashboard.html')

