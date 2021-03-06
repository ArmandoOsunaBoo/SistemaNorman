from django.contrib import admin
from employees.models import Employees, Attendance,Incidences
# Register your models here.

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    pass 
    list_display = ('old_number','number','name','group','jacket')
    list_display_links = ('number',)
    list_editable = ('name','group')
    search_fields = (
        'employees.number','employees.group','employees.jacket',
        'employees.name','employees.area'
    )
    list_filter = (
        'created',
        'modified'
    )
    readonly_fields = ('created','modified')

@admin.register(Incidences)
class IncidencesAdmin(admin.ModelAdmin):
    pass 
    list_display = ('incidence','number','date',
    'name','hours','minutes','day')
    list_display_links = ('number',)
    list_editable = ('name','date')
    list_filter = (
        'created',
        'modified'
    )
    readonly_fields = ('created','modified')