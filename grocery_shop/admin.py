from django.contrib import admin

from grocery_shop.models import Unit,Category,Shop,Product

# Register your models here.
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass 
    list_display = ('id','name','name_ch')
    list_display_links = ('name',)
    list_editable = ('name_ch',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass 
    list_display = ('id','name','name_ch')
    list_display_links = ('name',)
    list_editable = ('name_ch',)


    

@admin.register(Shop)
class CategoryAdmin(admin.ModelAdmin):
    pass 
    list_display = ('id','name','name_ch')
    list_display_links = ('name',)
    list_editable = ('name_ch',)




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass 
    list_display = ('name','name_ch','description','description_ch','price')
    list_display_links = ('name',)