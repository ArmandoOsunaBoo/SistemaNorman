
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from grocery_shop import views 


urlpatterns = [ 
    path(route='index/',view=views.index,name='shop'),
    path(route='menu/',view=views.menu,name='menu'),
    
    path(route='get_data/',view= views.ajax, name = "post_ajax"),
    path(route="detail/", view=views.detalles,name="detail"),
    path(route="cart/", view=views.cart,name="cart"),
    path(route="cart_update/", view=views.save_cart_items,name="cart_update"),
    path(route="cart_delete/", view=views.delete_cart_item,name="cart_delete"),
    path(route="insert_to_cart/", view=views.insert_to_cart,name="insert_to_cart"),

    path(route="get_item/", view=views.get_item,name="get_item"),


    path(route='manage/',view=views.manage,name='manage'),
    path(route='reports/',view=views.reports,name='reports'),
    
    path(route='out_service/',view=views.out_service,name='out_service')
]