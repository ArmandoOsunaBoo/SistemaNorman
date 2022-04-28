#Django imports
from ast import Return
from email.policy import default
from unicodedata import name
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.http.response import JsonResponse

#Personal imports
from employees.library.db_manager import create_day_attendance,upload_incidences,merge_payroll,upload_employees,create_employee_excel,upload_assistances,download_week_atendance,generate_payroll
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
from django.core.files.storage import default_storage

@login_required
def delete_employee(request):
    pass
    id_tax=(request.GET['id_tax'])
    instance = Employees.objects.get(id=id_tax)
    instance.delete()
    employees_list = Employees.objects.all()
    peg = Paginator(employees_list, 10)
    employees = peg.page(1).object_list
    
    lista = list(employees.values())
    jeison = json.dumps(lista,  ensure_ascii=True,default=str)
    return JsonResponse(jeison,status=200,safe=False)


@login_required
def get_names(request):
    pass
    
    text=(request.GET['text'])
    employees_list = Employees.objects.filter(status="Activo",name__icontains=text)
    peg = Paginator(employees_list, 10)
    employees = peg.page(1).object_list
    
    lista = list(employees.values())
    jeison = json.dumps(lista,  ensure_ascii=True,default=str)
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
        incidences = Incidences.objects.all()
        paginator = Paginator(incidences, 10)
        page = request.GET.get('page', 1)
        try:
            incidences = paginator.page(page)
        except PageNotAnInteger:
            incidences = paginator.page(1)
        except EmptyPage:
            incidences = paginator.page(paginator.num_pages)
        if  'carga_incidencias' in request.FILES:
            doc = request.FILES
            excel_file = doc["carga_incidencias"]
            upload_incidences(excel_file)

        if 'falta_checadas' in request.POST:
            d = request.POST.get('falta_checadas', None)
            create_day_attendance(d)
            fh = open("FaltaChecadas.xlsx", 'rb')
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('FaltaChecadas1.xlsx')
            return response   

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
            wb = Workbook()
            ws = wb.active
            download_week_atendance(date_1,end_date,wb,ws)
            wb.save("ReporteOrdenado.xlsx")
            fh = open("ReporteOrdenado.xlsx", 'rb')
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('ReporteOrdenado.xlsx')
            return response

        return render(request,'employees/attendance.html',{'incidences':incidences})

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
        if 'modal_form' in request.POST: 
            modal_form= request.POST["modal_form"] 
            if(modal_form=="0"):
                obj_e = Employees()
                obj_e.old_number = request.POST.get("emp_oldnumber","00000")
                obj_e.turn = request.POST.get("employee_turn","NA")
                obj_e.number = request.POST.get("emp_number","00000")
                obj_e.name = request.POST.get("emp_name","NO INGRESADA")
                obj_e.group =   request.POST.get("emp_group","NO INGRESADA")
                obj_e.team = request.POST.get("emp_team","NO INGRESADA")
                obj_e.personal =  request.POST.get("emp_personal","NO INGRESADA")
                obj_e.department_rp =   request.POST.get("emp_departament_rp","NO INGRESADA")
                obj_e.area_rp =   request.POST.get("emp_area_rp","NO INGRESADA")
                obj_e.position_rp =   request.POST.get("emp_position_rp","NO INGRESADA")
                obj_e.payroll = request.POST.get("emp_payroll","NO INGRESADA") 
                obj_e.admission_date =   request.POST.get("emp_admission_date","NO INGRESADA")
                obj_e.antiquity =  request.POST.get("emp_antiquity","NO INGRESADA")
                obj_e.status = request.POST.get("emp_status","NO INGRESADA")
                obj_e.leaving_date =  request.POST.get("emp_leaving_date","NO INGRESADA")
                obj_e.reason_of_leaving = request.POST.get("emp_reason_of_leaving","NO INGRESADA")
                obj_e.curp =  request.POST.get("emp_curp","NO INGRESADA")
                obj_e.rfc = request.POST.get("emp_rfc","NO INGRESADA")
                obj_e.nss =  request.POST.get("emp_nss","NO INGRESADA")
                #obj_e.e_age = request.POST.get("emp_age","0")
                obj_e.gender = request.POST.get("emp_gender","NO INGRESADA")
                obj_e.department =  request.POST.get("emp_department","NO INGRESADA")
                obj_e.position =  request.POST.get("emp_position","NO INGRESADA")

                obj_e.jacket = request.POST.get("emp_jacket","NA") 
                obj_e.aplication =  request.POST.get("emp_aplication","NO INGRESADA")
                obj_e.performance =  request.POST.get("emp_performance","NO INGRESADA")
                obj_e.birth_date =  request.POST.get("emp_birth_date","NO INGRESADA")
                obj_e.nacionality =  request.POST.get("emp_nationality","NO INGRESADA")
                obj_e.place_of_birth =  request.POST.get("emp_place_of_birth","NO INGRESADA")
                obj_e.municipality =  request.POST.get("emp_municipality","NO INGRESADA")
                obj_e.location = request.POST.get("emp_location","NO INGRESADA")
                obj_e.division =  request.POST.get("emp_division","NO INGRESADA")
                obj_e.suburb = request.POST.get("emp_suburb","NO INGRESADA")
                obj_e.street = request.POST.get("emp_street","NO INGRESADA")
                obj_e.house_number = request.POST.get("emp_house_number","NO INGRESADA")
                obj_e.studies = request.POST.get("emp_studies","NO INGRESADA")
                obj_e.email = request.POST.get("emp_email","NO INGRESADA")
                obj_e.phone = request.POST.get("emp_phone","NO INGRESADA")
                obj_e.blood_type = request.POST.get("emp_blood_type","NO INGRESADA")
                obj_e.allergies = request.POST.get("emp_allergies","NO INGRESADA")
                obj_e.marital_status = request.POST.get("emp_marital_status","NO INGRESADA")
                obj_e.route =  request.POST.get("emp_route","NO INGRESADA")
                obj_e.bus_stop =  request.POST.get("emp_bus_stop","NO INGRESADA")
                obj_e.emergency_phone_1 =  request.POST.get("emp_emergency_phone1","NO INGRESADA")
                obj_e.emergency_phone_2 =  request.POST.get("emp_emergency_phone2","NO INGRESADA")
                obj_e.emergency_phone_3 =  request.POST.get("emp_emergency_phone3","NO INGRESADA")
                obj_e.schedule = request.POST.get("emp_schedule","NO INGRESADA")
                obj_e.number_of_children = request.POST.get("emp_number_of_children","NO INGRESADA")
                obj_e.age_of_kid_1 =  request.POST.get("emp_kid1","NO INGRESADA")
                obj_e.age_of_kid_2 =  request.POST.get("emp_kid2","NO INGRESADA")
                obj_e.age_of_kid_3 = request.POST.get("emp_kid3","NO INGRESADA")
                obj_e.age_of_kid_4 =  request.POST.get("emp_kid4","NO INGRESADA")
                obj_e.age_of_kid_5 =  request.POST.get("emp_kid5","NO INGRESADA")
                obj_e.id_noi =  request.POST.get("emp_id_noi","NO INGRESADA")

                if len(request.FILES) != 0:
                    file = request.FILES['emp_picture']
                    filename = file.name
                    filename = obj_e.name
                    # instead of "filename" specify the full path and filename of your choice here
                    with default_storage.open('employees/'+filename+".jpeg", 'wb') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    obj_e.picture = filename
                else:
                    obj_e.picture = "NO INGRESADA"
                
                obj_e.boss_support = request.POST.get("emp_boss_support","NO INGRESADA")
                obj_e.relation =  request.POST.get("emp_relation","NO INGRESADA")
                
                obj_e.master_id = "NA"
                obj_e.save()

                page = request.GET['page']
                employees2 = Employees.objects.filter(status="Activo").exclude(number__contains='C00').order_by("-number")

                peg = Paginator(employees2, 100)
                employees = peg.page(page)
                return render(request,'employees/index.html',{"page":page,'employees': employees})
           
            if(modal_form=="1"):
                obj_e = Employees.objects.get(id=request.POST["emp_id"])
                obj_e.old_number = request.POST.get("emp_oldnumber","00000")
                obj_e.number = request.POST.get("emp_number","00000")
                obj_e.name = request.POST.get("emp_name","NO INGRESADA")
                obj_e.group =   request.POST.get("emp_group","NO INGRESADA")
                obj_e.team = request.POST.get("emp_team","NO INGRESADA")
                obj_e.personal =  request.POST.get("emp_personal","NO INGRESADA")
                obj_e.department_rp =   request.POST.get("emp_departament_rp","NO INGRESADA")
                obj_e.area_rp =   request.POST.get("emp_area_rp","NO INGRESADA")
                obj_e.position_rp =   request.POST.get("emp_position_rp","NO INGRESADA")
                obj_e.payroll = request.POST.get("emp_payroll","NO INGRESADA") 
                obj_e.admission_date =   request.POST.get("emp_admission_date","NO INGRESADA")
                obj_e.antiquity =  request.POST.get("emp_antiquity","NO INGRESADA")
                obj_e.status = request.POST.get("emp_status","Activo")
                obj_e.leaving_date =  request.POST.get("emp_leaving_date","NO INGRESADA")
                obj_e.reason_of_leaving = request.POST.get("emp_reason_of_leaving","NO INGRESADA")
                obj_e.curp =  request.POST.get("emp_curp","NO INGRESADA")
                obj_e.rfc = request.POST.get("emp_rfc","NO INGRESADA")
                obj_e.nss =  request.POST.get("emp_nss","NO INGRESADA")
                #obj_e.age = str(request.POST["emp_age"])
                obj_e.gender = request.POST.get("emp_gender","NO INGRESADA")
                obj_e.department =  request.POST.get("emp_department","NO INGRESADA")
                obj_e.position =  request.POST.get("emp_position","NO INGRESADA")
                obj_e.turn = request.POST.get("employee_turn","NA")
                obj_e.jacket = request.POST.get("emp_jacket","NA") 
                obj_e.aplication =  request.POST.get("emp_aplication","NO INGRESADA")
                obj_e.performance =  request.POST.get("emp_performance","NO INGRESADA")
                obj_e.birth_date =  request.POST.get("emp_birth_date","NO INGRESADA")
                obj_e.nacionality =  request.POST.get("emp_nationality","NO INGRESADA")
                obj_e.place_of_birth =  request.POST.get("emp_place_of_birth","NO INGRESADA")
                obj_e.municipality =  request.POST.get("emp_municipality","NO INGRESADA")
                obj_e.location = request.POST.get("emp_location","NO INGRESADA")
                obj_e.division =  request.POST.get("emp_division","NO INGRESADA")
                obj_e.suburb = request.POST.get("emp_suburb","NO INGRESADA")
                obj_e.street = request.POST.get("emp_street","NO INGRESADA")
                obj_e.house_number = request.POST.get("emp_house_number","NO INGRESADA")
                obj_e.studies = request.POST.get("emp_studies","NO INGRESADA")
                obj_e.email = request.POST.get("emp_email","NO INGRESADA")
                obj_e.phone = request.POST.get("emp_phone","NO INGRESADA")
                obj_e.blood_type = request.POST.get("emp_blood_type","NO INGRESADA")
                obj_e.allergies = request.POST.get("emp_allergies","NO INGRESADA")
                obj_e.marital_status = request.POST.get("emp_marital_status","NO INGRESADA")
                obj_e.route =  request.POST.get("emp_route","NO INGRESADA")
                obj_e.bus_stop =  request.POST.get("emp_bus_stop","NO INGRESADA")
                obj_e.emergency_phone_1 =  request.POST.get("emp_emergency_phone1","NO INGRESADA")
                obj_e.emergency_phone_2 =  request.POST.get("emp_emergency_phone2","NO INGRESADA")
                obj_e.emergency_phone_3 =  request.POST.get("emp_emergency_phone3","NO INGRESADA")
                obj_e.schedule = request.POST.get("emp_schedule","NO INGRESADA")
                obj_e.number_of_children = request.POST.get("emp_number_of_children","NO INGRESADA")
                obj_e.age_of_kid_1 =  request.POST.get("emp_kid1","NO INGRESADA")
                obj_e.age_of_kid_2 =  request.POST.get("emp_kid2","NO INGRESADA")
                obj_e.age_of_kid_3 = request.POST.get("emp_kid3","NO INGRESADA")
                obj_e.age_of_kid_4 =  request.POST.get("emp_kid4","NO INGRESADA")
                obj_e.age_of_kid_5 =  request.POST.get("emp_kid5","NO INGRESADA")
                obj_e.id_noi =  request.POST.get("emp_id_noi","NO INGRESADA")
                if len(request.FILES) != 0:
                    file = request.FILES['emp_picture']
                    filename = file.name
                    filename = obj_e.name
                    # instead of "filename" specify the full path and filename of your choice here
                    with default_storage.open('employees/'+filename+".jpeg", 'wb') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    obj_e.picture = filename
                else:
                    obj_e.picture = "NO INGRESADA"
                
                obj_e.boss_support = request.POST.get("emp_boss_support","NO INGRESADA")
                obj_e.relation =  request.POST.get("emp_relation","NO INGRESADA")
                
                obj_e.master_id = "NA"
                obj_e.save()

                page = request.GET['page']
                employees2 = Employees.objects.filter(status="Activo").exclude(number__contains='C00').order_by("-number")

                peg = Paginator(employees2, 100)
                employees = peg.page(page)
                return render(request,'employees/index.html',{"page":page,'employees': employees})
            if(modal_form==2):
                pass

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
        employees2 = Employees.objects.filter(status="Activo").exclude(number__contains='C00').order_by("-number")
        
        peg = Paginator(employees2, 100)
        employees = peg.page(page) 
        return render(request,'employees/index.html',{"page":page,'employees': employees})

    else:
        page = request.GET['page']
        employees2 = Employees.objects.filter(status="Activo").exclude(number__contains='C00').order_by("-number")

        peg = Paginator(employees2, 100)
        employees = peg.page(page)
        return render(request,'employees/index.html',{"page":page,'employees': employees})

@login_required
def get_employee(request):
    pass
    text=(request.GET['id']) 
    employees_list = Employees.objects.filter(id=text)
    jeison = json.dumps(list(employees_list.values()),  ensure_ascii=True,default=str)
    return JsonResponse(jeison,status=200,safe=False)