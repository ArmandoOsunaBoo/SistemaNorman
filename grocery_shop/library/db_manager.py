
#Django imports
from django.shortcuts import render,redirect

#Personal imports
from employees.models import Employees, Attendance
import xlrd
import datetime
from datetime import date
from openpyxl import load_workbook
from openpyxl import Workbook
import os
from PyPDF3 import PdfFileMerger
from grocery_shop.models import Product,Category,Unit,Shop
 

def upload_products_by_excel(excel_file):
    pass
    #utility
    offset = 1
    # you may put validations here to check extension or file size
    wb = xlrd.open_workbook(excel_file.temporary_file_path())
    # getting a particular sheet by name out of many sheets
    ws = wb.sheet_by_index(0)
    all_categories = Category.objects.all()
    all_shops = Shop.objects.all()
    all_units = Unit.objects.all()
    all_products = Product.objects.all()
    obj = Product()
    for i, row in enumerate(range(ws.nrows)):
            if i < offset:  
                continue
            r = []
            master = ws.cell(i, 0).value
            if not Category.objects.filter(name=ws.cell(i, 7).value).exists():
                pass
                obj = Category(name=ws.cell(i, 7).value,name_ch=ws.cell(i, 7).value)
                obj.save()
            if not Unit.objects.filter(name=ws.cell(i, 12).value).exists():
                pass
                obj = Unit(name=ws.cell(i, 12).value,name_ch =ws.cell(i,12).value)
                obj.save()
            if not Shop.objects.filter(name=ws.cell(i, 8).value).exists():
                pass
                obj = Shop(name=ws.cell(i, 8).value, name_ch =ws.cell(i, 8).value)
                obj.save()
                
            if Product.objects.filter(id_master=master).exists():
               pass
               #need to update the product
               obj = Product.objects.get(id_master=master)
               create_products(ws,i,obj)
            else:
                obj = Product()
                create_products(ws,i,obj)

def create_products(ws,i,obj):
    pass
    p=str(ws.cell(i,0).value)
    obj.id_master = p[:-2]
    obj.name = ws.cell(i, 2).value
    obj.name_ch = ws.cell(i, 3).value
    obj.description = ws.cell(i, 5).value
    obj.description_ch = ws.cell(i, 6).value
    p = str(ws.cell(i, 10).value)
    obj.price = p[:-2]
    print(p[:-2])
    obj.code = ws.cell(i, 9).value
    obj.image = ws.cell(i, 11).value+".jpg"
    objc = Category.objects.get(name=ws.cell(i, 7).value)
    obj.category_name_id = objc.id
    objc = Shop.objects.get(name=ws.cell(i, 8).value)
    obj.shop_name_id = objc.id
    objc = Unit.objects.get(name=ws.cell(i, 12).value)
    obj.unit_name_id = objc.id
    obj.save()

