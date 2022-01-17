from django.urls import path
from badge import views

urlpatterns = [
    path(route='badge/',view = views.badge_main,name="badge_main"),
]
