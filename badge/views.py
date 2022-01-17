from django.shortcuts import render

# Create your views here.
def badge_main(request):
    return render(request, 'badge/badge_main.html')