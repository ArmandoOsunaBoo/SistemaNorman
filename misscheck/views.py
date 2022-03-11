from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import letter, landscape
from django.http import HttpResponse, Http404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.db import connection
import pandas as pd
import itertools
import os

# Create your views here.
def misscheck(request):
    if "descargar" in request.POST:
        file_path = 'misscheck-file.pdf'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    elif "archivo" in request.FILES:
        excel_file = request.FILES["archivo"]
        df = pd.read_excel (excel_file,dtype=str)
        fecha_actual = df.columns[1]
        df = df.drop([0], axis=0)#Delete the firs row
        df.columns = ['Area','No.Empleado','Nombre','Falta Checadas','Autorización por falta de checadas','Firma']
        df = df.reset_index(drop=True)
        
        #Code to clean the data. We just keep the employees that have miss check
        body = {"Area":[],"No.Empleado":[],"Nombre":[],"Falta Checadas":[],"Autorización por falta de checadas":[],"Firma":[]}
        clean_data = pd.DataFrame(body)#DataSet Con datos Limpios (Solo perosnas con falta de checadas)
        for i in range(len(df)):
            if(str(df.at[i,'Falta Checadas'])!="nan"):
                clean_data = clean_data.append(df.iloc[i])
        
        #Order data by Área
        clean_data.sort_values(by=['Area'],inplace=True)
        #Complement the excel data with the database
        body_final = {"area":[],"nomina":[],"numero":[],"nombre":[],"faltas":[]}
        final_data = pd.DataFrame(body_final)
        for i in range(len(clean_data)):
            search = clean_data.iloc[i,1]
            cursor = connection.cursor()
            sql = f''' SELECT payroll, area_rp FROM employees_employees WHERE number =  {search}'''
            cursor.execute(sql)
            db_get = cursor.fetchone()
            final_data = final_data.append({ 'area':db_get[1] , 'nomina':db_get[0] , 'numero':clean_data.iloc[i,1] , 'nombre':clean_data.iloc[i,2] , 'faltas':clean_data.iloc[i,3]},ignore_index=True)
        split(fecha_actual,final_data)
        
        msg = "enabled",
        return render(request, 'misscheck/misscheck_main.html', {"msg":msg})
    else:
        msg = "disabled",
        return render(request, 'misscheck/misscheck_main.html', {"msg":msg})

#Function to split the Dataset by area
def split(fecha_actual,data):
    c = canvas.Canvas("misscheck-file.pdf", pagesize=landscape(letter))
    
    #Get the areas to search
    cat_areas = data['area'].unique()
    
    headers = {"area":[],"nomina":[],"numero":[],"nombre":[],"faltas":[]}
    #First we get the "Important" employees
    # Recursos Humanos - Limpieza - Higiene y Seguridad - Departamento Medico - Chofer - Sabine(00014) - Yu (00004)
    count_p = 0
    temp = pd.DataFrame(headers)
    for j in range(len(data)):
        if data.iloc[j,0] == 'RECURSOS HUMANOS' or data.iloc[j,0] == "LIMPIEZA" or data.iloc[j,0] == "HIGIENE Y SEGURIDAD" or data.iloc[j,0] == "DEPARTAMENTO MEDICO" or data.iloc[j,0] == "CHOFER":
            count_p = count_p+1
            temp = temp.append({'area':data.iloc[j,0],'nomina':data.iloc[j,1],'numero':data.iloc[j,2],'nombre':data.iloc[j,3],'faltas':data.iloc[j,4]},ignore_index=True)
            data.at[j,'nomina'] = "S"
        elif data.iloc[j,2] == '00014' or data.iloc[j,2] == "00004": #Special case for Yu and Sabine
            count_p = count_p+1
            temp = temp.append({'area':data.iloc[j,0],'nomina':data.iloc[j,1],'numero':data.iloc[j,2],'nombre':data.iloc[j,3],'faltas':data.iloc[j,4]},ignore_index=True)
            data.at[j,'nomina'] = "S"
    if(len(temp)>0):
        export_to_pdf_special(fecha_actual, "Mixto", c, temp)
    del temp

    #Code for the ones that no are nomina type A
    for i in range(len(cat_areas)):
        temp = pd.DataFrame(headers)
        for j in range(len(data)):
            if cat_areas[i] == data.iloc[j,0] and (data.iloc[j,1] == 'C' or data.iloc[j,1] == 'B'):
                count_p = count_p+1
                temp = temp.append({'area':data.iloc[j,0],'nomina':data.iloc[j,1],'numero':data.iloc[j,2],'nombre':data.iloc[j,3],'faltas':data.iloc[j,4]},ignore_index=True)
        if(len(temp)>0):
            export_to_pdf(fecha_actual,cat_areas[i],c,temp)
        del temp
    
    #Repit the process only with the nomia A
    for i in range(len(cat_areas)):
        temp = pd.DataFrame(headers)
        for j in range(len(data)):
            if cat_areas[i] == data.iloc[j,0] and data.iloc[j,1] == 'A':
                count_p = count_p+1
                temp = temp.append({'area':data.iloc[j,0],'nomina':data.iloc[j,1],'numero':data.iloc[j,2],'nombre':data.iloc[j,3],'faltas':data.iloc[j,4]},ignore_index=True)
        if(len(temp)>0):
            export_to_pdf(fecha_actual,cat_areas[i],c,temp)
        del temp
        
    c.save()

#Funcion para generar una tabla en PDF en base a un conjunto de datos
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)
def export_to_pdf(fecha_actual,area,c,data):
    w, h = landscape(letter)
    # Margin.
    x_offset = 40
    y_offset = 75
    # Space between rows.
    padding = 15
    
    #Set a font that admit the Chinese Characters
    font_chinese = 'STSong-Light' # from Adobe's Asian Language Packs
    pdfmetrics.registerFont(UnicodeCIDFont(font_chinese))

    c.setFont(font_chinese, 35) #choose your font type and font size

    #Title
    c.drawString(x_offset,h-y_offset,"Falta de checadas 每日未打卡紀錄")
    y_offset = y_offset + 30
    c.setFont(font_chinese, 10) #choose your font type and font size

    #Date
    d1 = fecha_actual
    c.drawString(w-100,h-70,d1)

    #Header
    xhead = [x_offset,360]
    yhead = [h-y_offset - 0*padding,h-y_offset - 1*padding]
    c.grid(xhead,yhead)
    c.drawString(x_offset,h-y_offset-padding+3,"Área: " + area)
    y_offset = y_offset + 15
    head_title = ['NOM','Num','Nombre','Falta de Checada','Firma','Nota']

    #Draw the grid in regard to the input data size
    xlist = [x + x_offset for x in [0, 35, 65, 320, 540, 630, 700]]
    ylist = [h - y_offset - (y*padding) for y in range(len(data)+2)]
    c.grid(xlist, ylist)

    #Draw the Strings inside of the grid using the input data
    xc=0
    yc=0
    for x in range(len(xlist)-1):
        for y in range(len(ylist)-1):
            if y==0:
                c.drawString(xlist[x] + 2, ylist[y] - padding + 3, head_title[xc])    
            else:
                if(x<=3):
                    c.drawString(xlist[x] + 2, ylist[y] - padding + 3, data.iloc[yc-1,xc+1])
            yc = yc+1
        yc = 0
        xc = xc+1

    #Draw the line fot the Signatures
    c.line(300,ylist[len(ylist)-1]-60,450,ylist[len(ylist)-1]-60)
    c.drawString(330,ylist[len(ylist)-1]-75,"Firma de Jefe de Grupo")
    c.line(500,ylist[len(ylist)-1]-60,650,ylist[len(ylist)-1]-60)
    c.drawString(540,ylist[len(ylist)-1]-75,"Firma de Encargado")
    c.showPage()

#Special format to export
def export_to_pdf_special(fecha_actual,area,c,data):
    w, h = landscape(letter)
    # Margin.
    x_offset = 40
    y_offset = 75
    # Space between rows.
    padding = 15
    
    #Set a font that admit the Chinese Characters
    font_chinese = 'STSong-Light' # from Adobe's Asian Language Packs
    pdfmetrics.registerFont(UnicodeCIDFont(font_chinese))

    c.setFont(font_chinese, 35) #choose your font type and font size

    #Title
    c.drawString(x_offset,h-y_offset,"Falta de checadas 每日未打卡紀錄")
    y_offset = y_offset + 30
    c.setFont(font_chinese, 10) #choose your font type and font size

    #Date
    d1 = fecha_actual
    c.drawString(w-100,h-70,d1)

    #Header
    xhead = [x_offset,360]
    yhead = [h-y_offset - 0*padding,h-y_offset - 1*padding]
    c.grid(xhead,yhead)
    c.drawString(x_offset,h-y_offset-padding+3,"Área: " + area)
    y_offset = y_offset + 15
    head_title = ['NOM','Num','Nombre','Falta de Checada','Firma','Nota']

    #Draw the grid in regard to the input data size
    xlist = [x + x_offset for x in [0, 35, 65, 320, 540, 630, 700]]
    ylist = [h - y_offset - (y*padding) for y in range((2*len(data))+2)]
    c.grid(xlist, ylist)

    #Draw the headers
    for x in range(len(xlist)-1):
        c.drawString(xlist[x] + 2, ylist[0] - padding + 3, head_title[x])
    #Draw the Strings inside of the grid using the input data
    xc=0
    yc=0
    for x in range(len(xlist)-3):
        for y in range(len(data)):
            c.drawString(xlist[2] + 2, ylist[2*(y)+1] - padding + 3, data.iloc[yc,0])
            c.drawString(xlist[x] + 2, ylist[2*(y+1)] - padding + 3, data.iloc[yc,xc+1])
            yc = yc+1
        yc = 0
        xc = xc+1

    #Draw the line fot the Signatures
    c.line(300,ylist[len(ylist)-1]-60,450,ylist[len(ylist)-1]-60)
    c.drawString(330,ylist[len(ylist)-1]-75,"Firma de Jefe de Grupo")
    c.line(500,ylist[len(ylist)-1]-60,650,ylist[len(ylist)-1]-60)
    c.drawString(540,ylist[len(ylist)-1]-75,"Firma de Encargado")
    c.showPage()