
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from employees import views 


urlpatterns = [  
    #management
    path(route='index/',view=views.employee_index,name='employees'),
    path(route='payroll/',view=views.employee_payroll,name='payroll'),
    path(route='attendance/',view=views.employee_attendance,name='attendance'),
]  