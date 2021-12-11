from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class Shop(models.Model):
    pass
    name = models.CharField(verbose_name='name', max_length=100, unique=True)
    name_ch = models.CharField(verbose_name='name_ch', max_length=100,null=True)
    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        ordering = ['-name']

    def __str__(self):
        return self.name


class Unit(models.Model):
    pass
    name = models.CharField(verbose_name='name', max_length=100, unique=True)
    name_ch = models.CharField(verbose_name='name_ch', max_length=100,null=True)
    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        ordering = ['-name']

    def __str__(self):
        return self.name

class Category(models.Model):
    pass
    name = models.CharField(verbose_name='name', max_length=100, unique=True)
    name_ch = models.CharField(verbose_name='name_ch', max_length=100,null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-name']

    def __str__(self):
        return self.name

class Product(models.Model):
    id_master = models.CharField(verbose_name='id_master', max_length=100,null=True)
    name = models.CharField(verbose_name='name', max_length=100,null=True)
    name_ch = models.CharField(verbose_name='name_ch', max_length=100,null=True)
    description = models.CharField(verbose_name='description', max_length=100,null=True)
    description_ch = models.CharField(verbose_name='description_ch', max_length=100,null=True)
    price = models.FloatField(verbose_name='price')
    code = models.CharField(verbose_name='code', max_length=100,null=False)
    image = models.ImageField(null=True,blank=True)
    
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE,unique=False)
    shop_name = models.ForeignKey(Shop,on_delete=models.CASCADE)
    unit_name = models.ForeignKey(Unit,on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-name']

    def __str__(self):
        return self.name

class Order(models.Model):
    pass
    date = models.DateField(verbose_name='fecha')
    amount = models.CharField(verbose_name='code', max_length=100,null=True)
    unit = models.CharField(verbose_name='code', max_length=100,null=True)
    product_name = models.CharField(verbose_name='code', max_length=100,null=True)
    id_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True) 
    user_name = models.CharField(verbose_name='code', max_length=100,null=True)
    unidad_cantidad = models.CharField(max_length=50,null=True)
    unit_price = models.CharField(verbose_name='code', max_length=100,null=True)
    
    def total_cost(self):
        return float(self.cantidad) * self.id_producto.price
  
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date']

    def __str__(self):
        return self.date+"-"+self.id_user


    CATEGORY_LIST = (
        ('SAMS', 'SAMS'),
        ('WALMART', 'WALMART'),
        ('KOREANO', 'KOREANO'),
        ('SR.WU', 'SR.WU'),
        ('COTSCO', 'COTSCO'),
        ('CHINA', 'CHINA'),
        ('VERDURAS', 'VERDURAS'),
        ('CARNE', 'CARNE'),
        ('MARISCOS', 'MARISCOS'),
        ('PAN ASIA', 'PAN ASIA'),
        ('FRUTAS', 'FRUTAS'),
        ('工作表', '工作表'),
    )
    
    UNIT_LIST = (
        ('PIEZAS', 'PIEZAS'),
        ('PIEZAS', 'PIEZAS'),
        ('KG', 'KG'),
        ('LB', 'LB'),
        ('LB', 'LB'),
    )

    SHOP_LIST = (
        ('SAMS', 'SAMS'),
        ('WALMART', 'WALMART'),
        ('KOREANO', 'KOREANO'),
        ('SR.WU', 'SR.WU'),
        ('COTSCO', 'COTSCO'),
        ('CHINA', 'CHINA'),
        ('VERDURAS', 'VERDURAS'),
        ('CARNE', 'CARNE'),
        ('MARISCOS', 'MARISCOS'),
        ('PAN ASIA', 'PAN ASIA'),
        ('FRUTAS', 'FRUTAS'),
        ('工作表', '工作表'),
    )