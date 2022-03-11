#Django imports
from ast import Return
from email.policy import default
from unicodedata import name
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.http.response import JsonResponse

#Personal imports
from employees.library.db_manager import upload_incidences,merge_payroll,upload_employees,create_employee_excel,upload_assistances,download_week_atendance,generate_payroll
import xlrd
import os
from openpyxl import Workbook
import datetime
from django.contrib.auth.decorators import login_required
from employees.models import Employees, Incidences
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import JsonResponse
import json
from django.core import serializers
from django.http import JsonResponse

@login_required
def get_names(request):
    pass
    print()
    
    text=(request.GET['text'])
    employees_list = Employees.objects.filter(status="Activo",name__icontains=text)
    peg = Paginator(employees_list, 10)
    employees = peg.page(1).object_list
    print("%%%%%%%%%%%%%%")
    
    lista = list(employees.values())
    print("***************************")
    print(type(lista))
    print(type(lista[0]))
    print(lista[0])
    jeison = json.dumps(lista,  ensure_ascii=True,default=str)
    print(type(jeison))
    return JsonResponse(jeison,status=200,safe=False)

@login_required
def get_incidences(request):
    pass

@login_required
def employee_payroll(request):
    pass
    if request.method == 'POST':
        if 'order_all_payrolls' in request.FILES:
            pass
            doc = request.FILES
            print(type(doc.getlist('order_all_payrolls')))
            merge_payroll(doc.getlist('order_all_payrolls'))

        if 'calculate_payroll' in request.FILES:
            pass
            doc = request.FILES
            excel_file = doc["calculate_payroll"]
            generate_payroll(excel_file)
    else:
        return render(request,'employees/payroll.html')


@login_required
def employee_attendance(request):
    pass
    if request.method == 'POST':

        if  'carga_incidencias' in request.FILES:
            doc = request.FILES
            excel_file = doc["carga_incidencias"]
            upload_incidences(excel_file)


        if  'carga_checadas' in request.FILES:
            doc = request.FILES
            excel_file = doc["carga_checadas"]
            upload_assistances(excel_file)
        
        if 'reporte_semanal' in request.POST:
            d = request.POST.get('reporte_semanal', None)
            
            r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
            format = "%Y-%m-%d %H:%M:%S"
            date_1 = datetime.datetime.strptime(str(r), format)
            end_date = date_1 + datetime.timedelta(days=5)
            date_1 = date_1 + datetime.timedelta(days=-1)
            date_1 = str(date_1)
            end_date = str(end_date)    
            # El documento
            wb = Workbook()
            # grab the active worksheet
            ws = wb.active
            download_week_atendance(date_1,end_date,wb,ws)
            wb.save("ReporteOrdenado.xlsx")
            fh = open("ReporteOrdenado.xlsx", 'rb')
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('ReporteOrdenado.xlsx')
            return response

        return render(request,'employees/attendance.html')

    else:
        incidences = Incidences.objects.all()
        paginator = Paginator(incidences, 10)
        page = request.GET.get('page', 1)
        try:
            incidences = paginator.page(page)
        except PageNotAnInteger:
            incidences = paginator.page(1)
        except EmptyPage:
            incidences = paginator.page(paginator.num_pages)
        return render(request,'employees/attendance.html',{'incidences':incidences})

#Logic for the view
@login_required
def employee_index(request):
    if request.method == 'POST':
            
        if 'upload_employees' in request.FILES:
            doc = request.FILES
            excel_file = doc["upload_employees"]
            wb = xlrd.open_workbook(excel_file.temporary_file_path())
            ws = wb.sheet_by_index(0)
            try:
                upload_employees(ws,wb)
            except Exception as e: print(e)
            
        if 'download_employees' in request.POST:
            wb = Workbook()
            ws = wb.active
            create_employee_excel(wb,ws)
            wb.save("FaltaChecadas.xlsx")
            fh = open("FaltaChecadas.xlsx", 'rb')
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('Reporte_Empleados.xlsx')
            return response
        
        page = request.GET['page']
        employees2 = Employees.objects.order_by("-number")
        
        peg = Paginator(employees2, 4)
        employees = peg.page(page)
        return render(request,'employees/index.html')

    else:
        page = request.GET['page']
        employees2 = Employees.objects.filter(status="Activo").exclude(number__contains='C00').order_by("-number")
        print(page)
        peg = Paginator(employees2, 100)
        employees = peg.page(page)
        print(page)
        return render(request,'employees/index.html',{"page":page,'employees': employees})

@login_required
def get_employee(request):
    pass
    text=(request.GET['id']) 
    employees_list = Employees.objects.filter(id=text)
    jeison = json.dumps(list(employees_list.values()),  ensure_ascii=True,default=str)
    return JsonResponse(jeison,status=200,safe=False)