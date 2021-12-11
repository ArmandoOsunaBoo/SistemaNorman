from django.contrib import admin


#Personal imports
from users.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    list_display = ('user','area','type','picture')
    list_display_links = ('user',)
    list_editable = ('area','type')
    search_fields = (
        'user.email','user.first_name','user.user_name',
        'user.last_name','user.area'
    )
    list_filter = (
        'created','user__is_active',
        'user__is_staff','modified'
    )

    fieldsets = (
        ('Profile', {
            "fields": (('user','picture'),),
        }),
        ('Extra info',{
            'fields':(
                ('area','type'),
            )
        }),
        ('Metadata',{
            'fields':(('created','modified'))
        })
    )
    readonly_fields = ('created','modified')


    #para unir profile con users cuando registren users
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    #se hace el registro"
    inlines = (ProfileInLine,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )

admin.site.unregister(User)
admin.site.register(User,UserAdmin)