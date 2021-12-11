#Django imports
from django.shortcuts import render,redirect
from django.http.response import HttpResponse

#Personal imports
from employees.library.db_manager import merge_payroll,upload_employees,create_employee_excel,upload_assistances,download_week_atendance,generate_payroll
import xlrd
import os
from openpyxl import Workbook
import datetime
from django.contrib.auth.decorators import login_required


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
     return render(request,'employees/attendance.html')

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
            
        return render(request,'employees/index.html')

    else:
        return render(request,'employees/index.html')

