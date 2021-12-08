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
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request,'users/login.html',{'error':'Invalid username or password'})
    return render(request,'users/login.html')

@login_required
def logout_view(request):
    pass
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    pass
    return render(request,'dashboard.html')

