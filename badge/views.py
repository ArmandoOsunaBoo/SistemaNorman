import os
from xml.dom import EMPTY_NAMESPACE
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from employees.models import Employees
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, landscape
from django.core.files.storage import default_storage

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def badge_main(request):
    if request.method == 'POST':
        nums = request.POST['numeros']
        employees = nums.split(",")
        global_offset = 580
        #Create the PDF file
        c = canvas.Canvas("clothe_badge.pdf", pagesize=(650,792))
        i=0
        for e in employees[:-1]:
            i = i+1
            draw(e,global_offset,c)
            global_offset = global_offset-161
            if i==4:
                i=0
                global_offset=580
                c.showPage()
        c.showPage()
        c.save()
    return render(request, 'badge/badge_main.html')

def robot(request):
    if request.method == 'GET':
        num = request.GET['data']
        employee_data = Employees.objects.filter(number__contains=num).values_list('name')
    try:
        response = {
            'status': 'True',
            'name': employee_data[0][0],
            'num': num
        }
        return JsonResponse(response,status=200,safe=False)
    except Exception as e:
        response = {
            'status': 'False',
            'msg': 'Nope'
        }
        return JsonResponse(response,status=200, safe=False)

def upload_photo(request):
    if request.method == 'POST':
        for upfile in request.FILES.getlist('photos'):
            filename = upfile.name
            # instead of "filename" specify the full path and filename of your choice here
            with default_storage.open('employees/'+filename, 'wb') as destination:
                for chunk in upfile.chunks():
                    destination.write(chunk)
    return render(request, 'badge/upload_photo.html')

# I found that the issue is with Pillow v6.0.0. Uninstalling it and doing pip install pillow==5.4.1 solved the issue for me.
def draw(num,global_offset,c):
    print(global_offset)
    datass = Employees.objects.filter(number__contains=num)
    num_emp = num
    nom = datass[0].name
    dep = datass[0].department_rp
    tel_emp = "4776897010"
    tel_eme_1 = datass[0].emergency_phone_1[:-2]
    tel_eme_2 = datass[0].emergency_phone_2[:-2]
    tel_eme_3 = datass[0].emergency_phone_3[:-2]
    nss = datass[0].nss
    tip_sangre = datass[0].blood_type
    alergias = datass[0].allergies
    rfc = datass[0].rfc
    curp = datass[0].curp
    fecha = datass[0].admission_date[:-9]

    #Use a Monospace font to can calculate the length
    pdfmetrics.registerFont(TTFont('courbd', 'courbd.ttf'))
    pdfmetrics.registerFont(TTFont('cour', 'cour.ttf'))

    x_offset = 47
    y_offset = global_offset#555#792-78(ofsset)-159(height)
    
    w, h = landscape(letter)#sheet size
    
    #Upload the images
    logo = ImageReader(os.path.join(BASE_DIR, 'badge\molde\Logo_Norman.png'))
    photo = ImageReader(os.path.join(BASE_DIR, "static\images\employees\\" + nom + ".jpeg"))

    #FRONT OUTLINE
    c.rect(x_offset+0,y_offset-0,259,159.5,1,0)
    #FRONT HEADER
    c.setFillColor("#284f6e")
    c.rect(x_offset+0,y_offset+119.6,259,39.8,1,1)
    c.drawImage(logo,x_offset+4,y_offset+119.6+4, 251, 31.8, mask='auto')
    #PHOTO OUTLINE
    c.rect(x_offset+149.41,y_offset+11.35,85.17,85.17,1,0)
    c.drawImage(photo,x_offset+149.41,y_offset+11.35,85.17,85.17,mask='auto')

#FRONT DATA
#NAME
    touse = 8.9/(len(nom))#Space by letter to use
    #fontsize = touse/0.0193#Calculated the font size divid it by EM(0.0193)
    fontsize = touse/0.0211#Calculated the font size divid it by EM(0.0193)
    # fontsize = math.floor(fontsize)
    if(fontsize>12):#Limit the font size
        fontsize=12
    space_used = ((fontsize*0.0211)*len(nom))#Calculated the space that use the name
    space_offset = ((9.1-space_used)*259)/8.9#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the name
    #Set the font
    c.setFont('courbd',fontsize)
    #Draw the string
    c.drawString(x_offset+space_offset,y_offset+102.5,nom)#Draw the name
#Num
    #Set the font
    c.setFont('cour',12)
    #Draw the string
    c.drawString(x_offset+21.75,y_offset+85.17,"N° EMPLEADO:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(num_emp))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+space_offset,y_offset+70.98,num_emp)#Draw the name
#Dep
    #Set the font
    c.setFont('cour',12)
    #Draw the string
    c.drawString(x_offset+17.98,y_offset+56.78,"DEPARTAMENTO:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(dep))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+space_offset,y_offset+42.58,dep)#Draw the name
#Tel
    #Set the font
    c.setFont('cour',11)
    #Draw the string
    c.drawString(x_offset+8.25,y_offset+28.39,"TELEFONO EMPRESA:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(tel_emp))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+space_offset,y_offset+14.19,tel_emp)#Draw the name



    #BACK OUTLINE
    c.rect(x_offset+260,y_offset-0,259,159.5,1,0)
    #BACK FOOTER
    c.setFillColor("#284f6e")
    c.rect(x_offset+260,y_offset,259,25.55,1,1)

#Tel 1
    #Set the font
    c.setFont('cour',9)
    #Draw the string
    c.drawString(x_offset+260+4.79,y_offset+147.64,"TELEFONO EMERGENCIA 1:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(tel_eme_1))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+260+space_offset,y_offset+133.44,tel_eme_1)#Draw the name
#Tel 2
    #Set the font
    c.setFont('cour',9)
    #Draw the string
    c.drawString(x_offset+260+4.79,y_offset+102.21,"TELEFONO EMERGENCIA 2:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(tel_eme_2))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+260+space_offset,y_offset+85.17,tel_eme_2)#Draw the name
#Tipo de Sangre
    #Set the font
    c.setFont('cour',8)
    #Draw the string
    c.drawString(x_offset+260+6.67,y_offset+56.78,"TIPO DE SANGRE/ALERGIAS:")#Draw the name

    tip_aler = tip_sangre + "/" + alergias

    touse = 4.3/(len(tip_aler))#Space by letter to use
    #fontsize = touse/0.0193#Calculated the font size divid it by EM(0.0193)
    fontsize = touse/0.0211#Calculated the font size divid it by EM(0.0193)
    # fontsize = math.floor(fontsize)
    if(fontsize>12):#Limit the font size
        fontsize=12

    #Calculate the offset
    space_used = ((fontsize*0.0211)*len(tip_aler))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',fontsize)
    #Draw the string
    c.drawString(x_offset+260+space_offset,y_offset+42.58,tip_aler)#Draw the name
#CURP
    #Set the font
    c.setFont('cour',10)
    #Draw the string
    c.drawString(x_offset+260+128+51.27,y_offset+133.44,"CURP:")#Draw the name
    #Calculate the offset
    space_used = ((11*0.0211)*len(curp))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',11)
    #Draw the string
    c.drawString(x_offset+260+128+space_offset,y_offset+119.25,curp)#Draw the name
#RFC
    #Set the font
    c.setFont('cour',10)
    #Draw the string
    c.drawString(x_offset+260+128+54.41,y_offset+85.17,"RFC:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(rfc))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+260+128+space_offset,y_offset+72.5,rfc)#Draw the name
#NSS
    #Set the font
    c.setFont('cour',10)
    #Draw the string
    c.drawString(x_offset+260+128+54.41,y_offset+42.58,"NSS:")#Draw the name
    #Calculate the offset
    space_used = ((12*0.0211)*len(nss))#Calculated the space that use
    space_offset = ((4.5-space_used)*128)/4.3#Remaining space in the template
    space_offset = space_offset/2#Divide the remaining space to center the text
    #Set the font
    c.setFont('courbd',12)
    #Draw the string
    c.drawString(x_offset+260+128+space_offset,y_offset+31.23,nss)#Draw the name
#FECHA
    #Set the font
    c.setFont('courbd',10)
    c.setFillColorRGB(1,1,1)
    #Draw the string
    c.drawString(x_offset+260+36.62,y_offset+11,"FECHA DE INGRESO: "+fecha)#Draw the name<