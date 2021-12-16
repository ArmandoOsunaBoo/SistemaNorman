
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from grocery_shop import views 


urlpatterns = [ 
    path(route='index/',view=views.index,name='shop'),
    path(route='menu/',view=views.menu,name='menu'),
    path(route='manage/',view=views.manage,name='manage'),
    path(route='get_data/',view= views.ajax, name = "post_ajax"),
    path(route="detalle/", view=views.detalles,name="detalle"),
] 

