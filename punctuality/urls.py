from django.urls import path
from punctuality import views

urlpatterns = [
    path(route='punctuality/',view = views.punctuality,name="punctuality"),
]