from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from django.http import HttpResponse, Http404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from datetime import datetime
import pandas as pd
import os

#Defines the check times
now = datetime.now().time()
start_time = now.replace(hour=8,minute=00,second=59,microsecond=0)
prefinish_time = now.replace(hour=17,minute=00,second=0,microsecond=0)
finish_time = now.replace(hour=17,minute=15,second=59,microsecond=0)
prestart_extra_time = now.replace(hour=17,minute=20,second=0,microsecond=0)
start_extra_time = now.replace(hour=17,minute=30,second=59,microsecond=0)
prefinish_extra_time = now.replace(hour=19,minute=30,second=0,microsecond=0)
finish_extra_time = now.replace(hour=19,minute=45,second=59,microsecond=0)
lunch_times = [[now.replace(hour=11,minute=30,second=0,microsecond=0),now.replace(hour=11,minute=55,second=59,microsecond=0),now.replace(hour=12,minute=30,second=59,microsecond=0),now.replace(hour=12,minute=15,second=0,microsecond=0)],
        [now.replace(hour=12,minute=0,second=0,microsecond=0),now.replace(hour=12,minute=25,second=59,microsecond=0),now.replace(hour=13,minute=00,second=59,microsecond=0),now.replace(hour=12,minute=45,second=0,microsecond=0)],
        [now.replace(hour=12,minute=30,second=0,microsecond=0),now.replace(hour=12,minute=55,second=59,microsecond=0),now.replace(hour=13,minute=30,second=59,microsecond=0),now.replace(hour=13,minute=15,second=0,microsecond=0)]]

# Create your views here.
def punctuality(request):
    if "descargar" in request.POST:
        file_path = 'punctuality-file.pdf'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    elif "archivo" in request.FILES:
        excel_file = request.FILES["archivo"]
        df = pd.read_excel (excel_file,dtype=str)
        df = df.drop([0], axis=0)#Delete the firs row
        df = df.drop([1], axis=0)#Delete the firs row
        df = df.reset_index(drop=True)
        df = df.drop(['EMPRESA','NOTA','NOTA.1','NOTA.2','NOTA.3','NOTA.4','NOTA.5'], axis=1)
        #print(df)
        
        #Code to clean the data. In the file exist employees that no longer work 
        
        #Process the data. First we split the dataset by employees, after we analize the time by employee
        split(df)
        
        msg = "enabled",
        return render(request, 'punctuality/punctuality_main.html', {"msg":msg})
    else:
        msg = "disabled",
        return render(request, 'punctuality/punctuality_main.html', {"msg":msg})

#Function to split the data by employees
def split(data):
    c = canvas.Canvas("punctuality-file.pdf", pagesize=landscape(letter))

    #Dataframes to save the employees times by category (MDF, Nomina A, Otros)
    final_body_data = {'NO':[],'NOMBRE':[],'DPTO':[],'LUNES':[],'MARTES':[],'MIERCOLES':[],'JUEVES':[],'VIERNES':[],'SABADO':[],'XLUNES':[],'XMARTES':[],'XMIERCOLES':[],'XJUEVES':[],'XVIERNES':[],'XSABADO':[],'FLAG1':[],'FLAG2':[]}
    type_a = pd.DataFrame(final_body_data)
    type_b = pd.DataFrame(final_body_data)
    type_c = pd.DataFrame(final_body_data)

    body_data = {'DPTO':[],'NO':[],'NOMBRE':[],'EVENTO':[],'LUNES':[],'MARTES':[],'MIERCOLES':[],'JUEVES':[],'VIERNES':[],'SABADO':[]}
    #each 8 columns are a new employee
    idx = 0
    type_nomina = ""
    for j in range(len(data)):
        #Initilize the dataframe
        if idx == 0:
            if str(data.iloc[j,0]) == "nan":
                break;
            split_data = pd.DataFrame(body_data)
            #Search the type of nomina to category the data
            cursor = connection.cursor()
            sql = f''' SELECT payroll,`group` FROM employees_employees WHERE number =  {data.iloc[j,1]}'''
            cursor.execute(sql)
            db_get = cursor.fetchone()
            type_nomina = db_get[0]
            type_area = db_get[1]
        #split the data by employee
        split_data = split_data.append({'DPTO':data.iloc[j,0],'NO':data.iloc[j,1],'NOMBRE':data.iloc[j,2],'EVENTO':data.iloc[j,3],'LUNES':data.iloc[j,4],'MARTES':data.iloc[j,5],'MIERCOLES':data.iloc[j,6],'JUEVES':data.iloc[j,7],'VIERNES':data.iloc[j,8],'SABADO':data.iloc[j,9]},ignore_index=True)
        idx = idx+1
        #Reset the temp dataframe to get another employee
        if idx == 8:
            miss_time, extra_miss_time, flags = checktime(split_data)
            #print(split_data)
            if type_nomina == "A":
                #print("Jenari")
                type_a = type_a.append({'NO':split_data.iloc[0,1],'DPTO':type_area,'NOMBRE':split_data.iloc[0,2],'LUNES':miss_time[0],'MARTES':miss_time[1],'MIERCOLES':miss_time[2],'JUEVES':miss_time[3],'VIERNES':miss_time[4],'SABADO':miss_time[5],'XLUNES':extra_miss_time[0],'XMARTES':extra_miss_time[1],'XMIERCOLES':extra_miss_time[2],'XJUEVES':extra_miss_time[3],'XVIERNES':extra_miss_time[4],'XSABADO':extra_miss_time[5],'FLAG1':flags[0],'FLAG2':flags[1]},ignore_index=True)
            elif type_area == "A MDF" or type_area == "B MDF" or type_area == "C MDF" or type_area == "D MDF":
                #print("Marco")
                type_b = type_b.append({'NO':split_data.iloc[0,1],'DPTO':type_area,'NOMBRE':split_data.iloc[0,2],'LUNES':miss_time[0],'MARTES':miss_time[1],'MIERCOLES':miss_time[2],'JUEVES':miss_time[3],'VIERNES':miss_time[4],'SABADO':miss_time[5],'XLUNES':extra_miss_time[0],'XMARTES':extra_miss_time[1],'XMIERCOLES':extra_miss_time[2],'XJUEVES':extra_miss_time[3],'XVIERNES':extra_miss_time[4],'XSABADO':extra_miss_time[5],'FLAG1':flags[0],'FLAG2':flags[1]},ignore_index=True)
            else:
                #print("Ana")
                type_c = type_c.append({'NO':split_data.iloc[0,1],'DPTO':type_area,'NOMBRE':split_data.iloc[0,2],'LUNES':miss_time[0],'MARTES':miss_time[1],'MIERCOLES':miss_time[2],'JUEVES':miss_time[3],'VIERNES':miss_time[4],'SABADO':miss_time[5],'XLUNES':extra_miss_time[0],'XMARTES':extra_miss_time[1],'XMIERCOLES':extra_miss_time[2],'XJUEVES':extra_miss_time[3],'XVIERNES':extra_miss_time[4],'XSABADO':extra_miss_time[5],'FLAG1':flags[0],'FLAG2':flags[1]},ignore_index=True)
            del split_data
            idx = 0

    #print("JENARI ------------------------------------------------")
    if len(type_a) != 0:
        #print(type_a)
        type_a.sort_values(by=['DPTO','NO'],inplace=True)
        export_to_pdf("Jenari",c,type_a)
    #print("MARCOS ------------------------------------------------")
    if len(type_b) != 0:
        #print(type_b)
        type_b.sort_values(by=['DPTO','NO'],inplace=True)
        export_to_pdf("Marcos",c,type_b)
    #print("ANA ------------------------------------------------")
    if len(type_c) != 0:
        #print(type_c)
        type_c.sort_values(by=['DPTO','NO'],inplace=True)
        export_to_pdf("Ana",c,type_c)
    c.save()

#Function to check the time
def checktime(data):
    #print(data)
    #Vector to save the wrong check time by day
    miss_check = ["","","","","",""]
    extra_miss_check = ["","","","","",""]
    flags = ["",""]
    #Variable to know if the employees miss
    falta_count=0
    extra_falta_count = 0
    extra_good_count = 0
    good_flag_count = 0
    extra_good_flag_count = 0
    #Get the area to verify the check time
    numero = data.iloc[0,1]
    cursor = connection.cursor()
    sql = f''' SELECT `group` FROM employees_employees WHERE number =  {numero}'''
    cursor.execute(sql)
    area = cursor.fetchone()

    #export_to_pdf(c,data)

    #Set the index to look for the time in regard to the area
    idxt = None
    if area[0] == "A MDF" or area[0] == "B MDF" or area[0] == "C MDF" or area[0] == "D MDF" or area[0] == "GRUPO DE CARTON" or area[0] == "ADMINISTRACION DE PRODUCCION" or area[0] == "GRUPO DE EXTRUSION" or area[0] == "MATERIALES" or area[0] == "GRUPO DE PREPARACION MDF":
        idxt = 0
    elif area[0] == "ADMINISTRACION" or area[0] == "RECURSOS HUMANOS" or area[0] == "IMPO / EXPO" or area[0] == "COMPRAS" or area[0] == "ASUNTOS GENERALES" or area[0] == "INVESTIGACION DE PRODUCCION" or area[0] == "INGENIERIA" or area[0] == "SISTEMAS" or area[0] == "DEPARTAMENTO MEDICO" or area[0] == "CONTROL DE PRODUCCION" or area[0] == "TRADUCCION" or area[0] == "FINANZAS" or area[0] == "PROGRAMACION DIARIA" or area[0] == "HIGIENE Y SEGURIDAD" or area[0] == "ADMINISTRACION DE PRODUCCION-1" or area[0] == "GRUPO DE EXTRUSION-1" or area[0] == "MATERIALES-1" or area[0] == "CHOFER" or area[0] == "CARGADOR" or area[0] == "LIMPIEZA":
        idxt = 1
    elif area[0] == "GRUPO DE ENSAMBLE I.M." or area[0] == "GRUPO DE PREPARACION I.M." or area[0] == "ADMINISTRACION DE PRODUCCION-2" or area[0] == "GRUPO DE EXTRUSION-2" or area[0] == "MATERIALES-2":
        idxt = 2
    #Verify the base time
    entrada = None
    ecomida = None
    scomida = None
    salida = None
    etextra = None
    stextra = None
    for j in range(6):
        #if j == 0: print("Lunes")
        #if j == 1: print("Martes")
        #if j == 2: print("Miercoles")
        #if j == 3: print("Jueves")
        #if j == 4: print("Viernes")
        #if j == 5: print("Sabado")
        for i in range(6):
            if i == 0:#Entrada
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    falta_count = falta_count + 1
                    miss_check[j] = miss_check[j] + "E:X "
                else:
                    entrada = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    if entrada <= start_time:
                        #print(data.iloc[i,j+4] + " Bien")
                        good_flag_count = good_flag_count + 1
                        miss_check[j] = miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        miss_check[j] = miss_check[j] + "E:"+data.iloc[i,j+4]+" "
            elif i == 1:#Entrada a Comer
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    falta_count = falta_count + 1
                    miss_check[j] = miss_check[j] + "SD:X "
                    #miss_check[j] = miss_check[j] + ""
                else:
                    ecomida = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    #print(ecomida)
                    #print(lunch_times[idxt][0])
                    #print(lunch_times[idxt][1])
                    if ecomida >= lunch_times[idxt][0] and ecomida <= lunch_times[idxt][1]:
                        #print(data.iloc[i,j+4] + " Bien")
                        miss_check[j] = miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        miss_check[j] = miss_check[j] + "SD:"+data.iloc[i,j+4]+" "
                        #miss_check[j] = miss_check[j] + ""
            elif i == 2:#Salida de Comer
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    falta_count = falta_count + 1
                    miss_check[j] = miss_check[j] + "ED:X "
                    #miss_check[j] = miss_check[j] + ""
                else:
                    scomida = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    if scomida >= lunch_times[idxt][3] and scomida <= lunch_times[idxt][2]:
                        #print(data.iloc[i,j+4] + " Bien")
                        miss_check[j] = miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        miss_check[j] = miss_check[j] + "ED:"+data.iloc[i,j+4]+" "
                        #miss_check[j] = miss_check[j] + ""
            elif i == 3:#Salida
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    falta_count = falta_count + 1
                    miss_check[j] = miss_check[j] + "S:X "
                else:
                    salida = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    if salida >= prefinish_time and salida <= finish_time:
                        #print(data.iloc[i,j+4] + " Bien")
                        good_flag_count = good_flag_count + 1
                        miss_check[j] = miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        miss_check[j] = miss_check[j] + "S:"+data.iloc[i,j+4]+" "
            elif i == 4 :#Entrada Tiempo Extra
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    extra_falta_count = extra_falta_count + 1
                    extra_miss_check[j] = extra_miss_check[j] + "ETE:X "
                    extra_good_flag_count = extra_good_flag_count + 1
                else:
                    etextra = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    if etextra >= prestart_extra_time and etextra <= start_extra_time:
                        #print(data.iloc[i,j+4] + " Bien")
                        extra_good_count = extra_good_count + 1
                        extra_miss_check[j] = extra_miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        extra_miss_check[j] = extra_miss_check[j] + "ETE:"+data.iloc[i,j+4]+" "
            elif i == 5:#Salida Tiempo Extra
                if str(data.iloc[i,j+4]) == "nan":
                    #print("NO HAY")
                    extra_falta_count = extra_falta_count + 1
                    extra_miss_check[j] = extra_miss_check[j] + "STE:X "
                    extra_good_flag_count = extra_good_flag_count + 1
                else:
                    stextra = datetime.strptime(data.iloc[i,j+4], '%H:%M:%S').time()
                    if stextra >= prefinish_extra_time and stextra <= finish_extra_time:
                        #print(data.iloc[i,j+4] + " Bien")
                        extra_good_count = extra_good_count + 1
                        extra_miss_check[j] = extra_miss_check[j] + ""
                    else:
                        #print(data.iloc[i,j+4] + " Mal")
                        extra_miss_check[j] = extra_miss_check[j] + "STE:"+data.iloc[i,j+4]+" "
        if falta_count == 4:
            miss_check[j] = "FALTO"
        falta_count = 0
        if extra_falta_count == 2:
            extra_miss_check[j] = "NO EXTRA"
        if extra_good_count == 2:
            extra_miss_check[j] = " EXTRA"
        extra_falta_count = 0
        extra_good_count = 0

    #Meaning that the employee check all right
    if good_flag_count == 12:
        flags[0] = "OK"
    #Meaning that the employee have not extra time
    if extra_good_flag_count == 12:
        flags[1] = "OK"
    return miss_check, extra_miss_check, flags
    #test = data.iloc[0,4]
    #print(test)

    #datetime_str = test
    #datetime_object = datetime.strptime(datetime_str, '%H:%M:%S').time()
    #print(datetime_object)

def export_to_pdf(name,c,data):
    w, h = landscape(letter)
    # Margin.
    x_offset = 40
    y_offset = 55
    # Space between rows.
    padding = 15
    
    #Set a font that admit the Chinese Characters
    font_chinese = 'STSong-Light' # from Adobe's Asian Language Packs
    pdfmetrics.registerFont(UnicodeCIDFont(font_chinese))

    #c.setFont(font_chinese, 35) #choose your font type and font size

    #Title
    #c.drawString(x_offset,h-y_offset,"Falta de checadas 每日未打卡紀錄")
    #y_offset = y_offset + 30
    c.setFont(font_chinese, 10) #choose your font type and font size

    #Date
    #d1 = fecha_actual
    c.drawString(w-100,h-40,name)

    #Header
    #xhead = [x_offset,360]
    #yhead = [h-y_offset - 0*padding,h-y_offset - 1*padding]
    #c.grid(xhead,yhead)
    #c.drawString(x_offset,h-y_offset-padding+3,"Área: ")
    #y_offset = y_offset + 15
    #head_title = ['NOM','Num','Nombre','Falta de Checada','Firma','Nota']

    tt = ["00050","MARIA DEL CARMEN ESPAÑA CABRERA TRONCOSO","ADMINISTRACCION DE PRODUCCION"]
    data_test = ["E:07:42:09","S:07:42:09","","E:07:42:09 - S:07:42:09 - EC:07:42:09","","FALTO"]
    data_test2 = ["E:07:42:09","","E:07:42:09 - S:07:42:09","","",""]
    day_hearders = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"]

    #Draw the grid in regard to the input data size
    h = h - y_offset;
    xlist = [x + x_offset for x in [0, 35, 373, 708]]
    xlist2 = [x + x_offset for x in [0, 118, 236, 354, 472, 590, 708]]

    max_rows = 0
    for i in range(len(data)):
        if data.iloc[i,15] == "" or data.iloc[i,16] == "":

            c.setFont(font_chinese, 10) #choose your font type and font size
            #Draw cell to headers
            max_rows = max_rows+1
            ylist = [h, h-padding]
            c.grid(xlist, ylist)
            #Fill the headers
            for j in range(3):
                c.drawString(xlist[j] + 2, h - padding + 3, data.iloc[i,j])
            #Draw cell to day hearders
            h = h - padding
            ylist = [h, h-padding]
            c.grid(xlist2, ylist)
            #Fill the day headrers
            for j in range(6):
                c.drawString(xlist2[j] + 2, h - padding + 3, day_hearders[j])
            h = h - padding
            #If data is null dont print the cells
            if data.iloc[i,15] == "":
                #Draw cell to data
                ylist = [h, h-padding]
                c.grid(xlist2,ylist)
                #Fill the cell data
                c.setFont(font_chinese, 8) #choose your font type and font size
                for j in range(6):
                    c.drawString(xlist2[j] + 2, h - padding + 3, data.iloc[i,j+3])
                h = h -padding
            if data.iloc[i,16] == "":
                #Draw cell to data
                ylist = [h, h-padding]
                c.grid(xlist2,ylist)
                #Fill the cell data
                c.setFont(font_chinese, 8) #choose your font type and font size
                for j in range(6):
                    c.drawString(xlist2[j] + 2, h - padding + 3, data.iloc[i,j+9])
                h = h -padding#Space between employees
            h = h - 8
            #Reset the values to draw in a new sheet
            if(h < 80):
                c.showPage()
                #c.setFont(font_chinese, 10) #choose your font type and font size
                h = 537
                max_rows=0
    c.showPage()