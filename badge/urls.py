from django.urls import path
from badge import views

urlpatterns = [
    path(route='badge/',view = views.badge_main,name="badge_main"),
    path(route='photo/',view = views.upload_photo,name="upload_photo"),
    path(route='robot/',view = views.robot,name="robot_act"),
]
