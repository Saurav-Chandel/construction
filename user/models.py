from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import django
# Create your models here.

worker_type = [
    ('supervisor', 'supervisor'),
    ('labour', 'labour'),
]
status = [
    ('pending', 'pending'),
    ('completed', 'completed'),
]
material_type = [
    (None, 'Select Material Type'),
    ('Cement', 'Cement'),
    ('Fine Sand', 'FIne Sand'),
    ('Course Sand', 'Course Sand'),
    ('Crusher Sand', 'Crusher Sand'),
    ('Course aggrigate 20mm', 'Course aggrigate 20mm'),
    ('Course aggrigate 40mm', 'Course aggrigate 40mm'),
    ('Course aggrigate 80mm', 'Course aggrigate 80mm'),
    ('Boulder', 'Boulder'),
    ('Bricks', 'Bricks'),
    ('CutStone', 'CutStone'),
    ('Re-bar', 'Re-bar'),
    ('Ms Steel', 'Ms Steel'),
    ('Ms-Pipe', 'Ms-Pipe'),
]
units = [
    (None, 'Select Unit'),
    ('Kg', 'Kg'),
    ('Bags', 'Bags'),
    ('Tipper', 'Tipper'),
    ('Truck', 'Truck'),
    ('Tonnes', 'Tonnes'),
    ('Quintal', 'Quintal'),
    ('Piece', 'box'),
    ('points', 'points'),
    ('Piece', 'Piece'),
    ('Troley', 'Troley'),
]
attendence = [
    ('1', 'present'),
    ('0', 'absent'),
    ('2', 'half_day'),
]

class User(AbstractUser):
     username = models.CharField(max_length=100, null=True,blank=True,unique=True)
     email=models.EmailField(max_length=250,unique=True,blank=True,null=True)
     password=models.CharField(max_length=100,null=True,blank=True)
     password2=models.CharField(max_length=100,null=True,blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
            return str(self.first_name)

class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=250,blank=True,null=True)
    budget=models.CharField(max_length=250,blank=True,null=True)
    status=models.CharField(max_length=250,default='pending',choices=status,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.title


class Worker(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,blank=True,null=True)  
    image=models.ImageField(upload_to='woker_image',null=True,blank=True)
    worker_type=models.CharField(max_length=100,choices=worker_type,blank=True,null=True)
    worker_wages=models.IntegerField(blank=True,null=True)
    # attendence=models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #         return str(self.name)

class Attendence(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
    attendence=models.CharField(max_length=100,choices=attendence,blank=True,null=True,default=1)
    today=models.DateField(auto_now_add=True,null=True,blank=True)
    money_paid=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.project.title)

class Retailer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=250,null=True,blank=True)  
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    shop_name=models.CharField(max_length=100,null=True,blank=True)
    vehicle_number=models.CharField(max_length=100,null=True,blank=True)
    total_ammount=models.IntegerField(blank=True,null=True)
    money_paid=models.IntegerField(blank=True,null=True)
    amount_to_pay=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
            return self.name
        
class Material(models.Model):
    paid=models.BooleanField(default=False,null=True,blank=True)
    retailer=models.ForeignKey(Retailer,on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    manual_material_type=models.CharField(max_length=250,null=True,blank=True)
    material_type=models.CharField(max_length=250,choices=material_type,null=True,blank=True)    
    quantity=models.CharField(max_length=250,null=True,blank=True)
    figure=models.IntegerField(blank=True,null=True)
    unit=models.CharField(max_length=250,null=True,blank=True,choices=units)
    size=models.CharField(max_length=100,null=True,blank=True)
    purpose=models.CharField(max_length=500,null=True,blank=True)
    price_per_item=models.CharField(max_length=100,blank=True,null=True)
    # item_Price_per_foot=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField(blank=True,null=True)
    money_paid=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs): 
        self.quantity = str(self.figure) +' '+ self.unit 
        try:
           self.total_price = int(self.price_per_item) * int(self.figure)
        except:
            pass   

        super(Material, self).save(*args, **kwargs)
        
class D_T(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    date_time= models.DateTimeField(auto_now_add=False,null=True,blank=True)
    date_time_auto_now_false= models.DateTimeField(auto_now=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    d=models.DateField(auto_now_add=False,null=True,blank=True)
    t=models.TimeField(auto_now_add=False,null=True,blank=True)

    cc=models.DateTimeField(auto_now_add=False,null=True,blank=True)





