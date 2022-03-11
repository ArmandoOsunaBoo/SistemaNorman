from django.shortcuts import render
from django.db import connection
from datetime import datetime
from django.http import JsonResponse
from .models import Consultas, Diccionario, Diagnosticos
from django.db.models import Q
import django_excel as excel
import calendar

# Create your views here.
def consulta(request):
    if not request.POST:
        print("Nothing")
    elif request.POST['cause'] and not 'save' in request.POST:
        search = request.POST['cause']
        search = search.rstrip()
        #print(search)
        cursor = connection.cursor()
        sql = f''' SELECT cause, diagnosis, therapy FROM nursing_diccionario WHERE UPPER(cause) = UPPER('{search}') '''
        cursor.execute(sql)
        db_get = cursor.fetchone()
        sql = f''' SELECT llave FROM nursing_diagnosticos WHERE nombre = "{search}" '''
        #print(sql)
        cursor.execute(sql)
        db_get2 = cursor.fetchone()
        data = [request.POST['number'],request.POST['name'],request.POST['area']]
        return render(request, 'nursing/consulta_main.html', {"data":data,"data_cause":db_get,"fallo":search,"cause_key":db_get2[0]})
    elif request.POST['number'] and not 'save' in request.POST:
        #print("SEARCH")
        search = request.POST['number']
        cursor = connection.cursor()
        sql = f''' SELECT number, name, area_rp FROM employees_employees WHERE number =  {search}'''
        cursor.execute(sql)
        db_get = cursor.fetchone()
        #print(db_get)
        return render(request, 'nursing/consulta_main.html', {"data":db_get})
    if 'save' in request.POST:
        fecha = datetime.now()
        key = request.POST['key']
        cause = request.POST['cause']
        diagnosis = request.POST['diagnosis']
        therapy = request.POST['therapy']
        cursor = connection.cursor()
        sql = f''' INSERT INTO nursing_diccionario VALUES(NULL,'{cause}','{diagnosis}','{therapy}') '''
        try:
            cursor.execute(sql)
        except:
            None
        number = request.POST['number']
        name = request.POST['name']
        area = request.POST['area']
        extra = request.POST['extra']
        notes = request.POST['notes']
        sql = f''' INSERT INTO nursing_consultas VALUES (NULL,"{number}","{key}","{cause}","{diagnosis}","{therapy}","Doc Diego + Enf Adriana","{notes}","{extra}","{fecha}","{fecha}") '''
        #print(sql)
        cursor.execute(sql)
        msg = "Saved!"
        return render(request, 'nursing/consulta_main.html', {"mytext":msg})
    return render(request, 'nursing/consulta_main.html')

def history(request):
    if 'buscar' in request.GET:
        search = request.GET['table_search']
        month = request.GET['month_c']
        month2 = request.GET['month_d']

        if(month!=""):
            if(month2==""):
                month2 = month
            month = month + "-01"
            month2 = month2 + "-" + str(calendar.monthrange(int(month2[0:4]), int(month2[5:7]))[1])
            data = Consultas.objects.filter( (Q(num__contains=search) | 
                                            Q(cause__contains=search) |
                                            Q(diagnosis__contains=search) |
                                            Q(therapy__contains=search) |
                                            Q(note__contains=search) |
                                            Q(llave__contains=search) |
                                            Q(extra__contains=search)) &
                                            Q(created__gte=month,created__lte=month2)).order_by('-created')
        else:
            data = Consultas.objects.filter( (Q(num__contains=search) | 
                                            Q(cause__contains=search) |
                                            Q(diagnosis__contains=search) |
                                            Q(therapy__contains=search) |
                                            Q(note__contains=search) |
                                            Q(llave__contains=search) |
                                            Q(extra__contains=search))).order_by('-created')
    elif 'download' in request.GET:
        month = request.GET['month_c']
        month2 = request.GET['month_d']

        if(month!=""):
            if(month2==""):
                month2 = month
            month = month + "-01"
            month2 = month2 + "-" + str(calendar.monthrange(int(month2[0:4]), int(month2[5:7]))[1])
            data = Consultas.objects.filter( Q(created__gte=month,created__lte=month2)).order_by('-created')
        else:
            data = Consultas.objects.all().order_by('-created')
        export=[]
        export.append(['Numero','Key','Motivo','Diagnostico','Tratamiento','Atendio','Llegada','Salida','Observaciones','Extra'])
        for result in data:
            export.append([result.num,result.llave,result.cause,result.diagnosis,result.therapy,result.doctor,
            result.created.replace(tzinfo=None),result.updated.replace(tzinfo=None),result.note,result.extra])
        today    = datetime.now()
        strToday = today.strftime("%d-%m-%y")

        # se transforma el array a una hoja de calculo en memoria
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, "xlsx", file_name="citas-"+strToday+".xlsx")
    else:
        data = Consultas.objects.all().order_by('-created')
    return render(request, 'nursing/history_main.html',{'datas':data})

def dictionary(request):
    if 'buscar' in request.GET:
        search = request.GET['table_search']
        data = Diccionario.objects.filter( Q(cause__contains=search) |
                                            Q(diagnosis__contains=search) |
                                            Q(therapy__contains=search)).order_by('-cause')
    elif 'download' in request.GET:
        data = Diccionario.objects.all()
        export=[]
        export.append(['Motivo','Diagnostico','Tratamiento'])
        for result in data:
            export.append([result.cause,result.diagnosis,result.therapy])
        today    = datetime.now()
        strToday = today.strftime("%d-%m-%y")

        # se transforma el array a una hoja de calculo en memoria
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, "xlsx", file_name="dictionary-"+strToday+".xlsx")
    else:
        print("else")
        data = Diccionario.objects.all().order_by('-cause')
    return render(request, 'nursing/dictionary_main.html',{'datas':data})

def search_cause(request):
    address = request.GET.get('cause')
    payload = []
    if len(address)>5:
        cause_objs = Diagnosticos.objects.filter(nombre__icontains=address)
        
        for cause_obj in cause_objs:
            payload.append(cause_obj.nombre)


    return JsonResponse({'status' : 200 , 'data' : payload})