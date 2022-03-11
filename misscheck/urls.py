from django.urls import path
from misscheck import views

urlpatterns = [
    path(route='misscheck/',view = views.misscheck,name="misscheck"),
]