from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
import datetime

# from rest_framework.response import Response

# Create your views here.

def Login(request):
    form = LoginForm(request.POST or None)

    msg = None
    if request.method=="GET":
        return render(request, "registration/login.html", {"form": form, "msg": msg})
        
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            print(username)
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "registration/login.html", {"form": form, "msg": msg})



def Signup(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form, "msg": msg, "success": success})   

def logout_view(request):
    logout(request)
    return redirect('/')     


@login_required(login_url="/login/")
def index(request):
    project=Project.objects.all().count()
    worker=Worker.objects.all().count()

    context = {'segment': 'index','project':project,'worker':worker}
    return render(request,'admin/home.html',context)

    # html_template = loader.get_template('admin/home.html')
    # return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def Profile(request):
    return render(request,'admin/profile.html',{'segment':'profile'})   

@login_required(login_url="/login/")
def Add_Project(request):
    if request.method=="GET":
        project=Project.objects.filter(user=request.user).order_by('-id')
        return render(request,'admin/project.html',{'project':project,'segment':'project'})
    if request.method=="POST":
        project_name=request.POST.get('project_name')
        budget=request.POST.get('budget')
        project=Project.objects.create(title=project_name,budget=budget,user=request.user)
        messages.add_message(request, messages.INFO, 'Project Created Successfully')
        return redirect('add_project')  

from django.db.models import Count,Sum
def Show_Material(request,id): 
    project=Project.objects.get(id=id)

    if request.method == "GET":
        retailer=Retailer.objects.all()
        form = ShowMaterialForm()
        material=Material.objects.filter(project=id).order_by('-id')
        # m_r=Material.objects.filter(project=id,retailer=8)
        # print(m_r)
        try:
            for i in material:
                if i.total_price==i.money_paid:
                    i.paid=True
                else:
                    i.paid=False    
                i.save()
        except:
            pass        
        #this is very simple approach
        # tt=Material.objects.filter(project=id).aggregate(Sum('total_price'))
        # print(tt['total_price__sum'])

        #In this approach we can not need to handel exceptioon case if there is no entry exists. it stores 0 value.
        # total_ammount=sum(x.total_price for x in material if x.total_price is not None)
        # ammount_paid=sum(x.money_paid for x in material if x.money_paid is not None)
        # ammount_to_pay=total_ammount-ammount_paid

        #Another Way to calculate total_ammount,ammount_paid,ammount_to_pay (in this approach we have to handel exceptional case)
        total_ammount=Project.objects.annotate(Sum('material__total_price')).filter(id=id)[0].material__total_price__sum
        ammount_paid=Project.objects.annotate(Sum('material__money_paid')).filter(id=id)[0].material__money_paid__sum
        
        if total_ammount and ammount_paid:
            ammount_to_pay=total_ammount-ammount_paid    
        else:
            ammount_to_pay=total_ammount  
        # print(material.values())    
        return render(request, 'admin/show_material.html', {"form": form,'material':material,'retailer':retailer,'project':project,'total_ammount':total_ammount,'ammount_paid':ammount_paid,'ammount_to_pay':ammount_to_pay})  

    if request.method=='POST':
        project=Project.objects.get(id=id)
        fm=ShowMaterialForm(request.POST)
        if fm.is_valid():
             m_t=fm.cleaned_data['material_type']
             m_m_t=fm.cleaned_data['manual_material_type']
             figure=fm.cleaned_data['figure']
             unit=fm.cleaned_data['unit']
             price_per_item=fm.cleaned_data['price_per_item']
            #  money_paid=fm.cleaned_data['money_paid']
             purpose=fm.cleaned_data['purpose']
             size=fm.cleaned_data['size']
             retailer=fm.cleaned_data['retailer']
            #  project=fm.cleaned_data['project']
             mat=Material(retailer=retailer,material_type=m_t,manual_material_type=m_m_t,figure=figure,unit=unit,price_per_item=price_per_item,size=size,purpose=purpose,project=project)
             mat.save()
             fm = ShowMaterialForm()  
             messages.add_message(request, messages.INFO, 'Material added successfully')
             return redirect('show_material',id=id)    

def Delete_Project(request,id):
    try:
        project=Project.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, 'Project Deleted Successfully')
        return redirect('add_project')    
    except:
        return redirect('add_project') 

def Get_Previous_Project(request,id):
    if request.is_ajax():
        project=Project.objects.get(id=id)
        data={
            'project_title':project.title,
            'project_budget':project.budget 
        }
        return JsonResponse(data)   

def Edit_Project(request):
    project=Project.objects.get(id=request.POST.get('project_id'))
    if request.POST.get('edit_name'):
        project.title=request.POST.get('edit_name')
    if request.POST.get('edit_budget'):
        project.budget=request.POST.get('edit_budget')
    project.save()    
    messages.add_message(request, messages.INFO, 'Project Updated Successfully')
    return redirect('add_project')         

@login_required(login_url="/login/")
def Add_Worker(request):
    projects=Project.objects.filter(user=request.user).order_by('-id')
    if request.method=="GET":
        worker=Worker.objects.filter(project__user=request.user).order_by('-id')
        attendence=Attendence.objects.filter(today=datetime.datetime.now().date(),attendence=1)

        return render(request,'admin/worker.html',{'project':projects,'workers':worker,'attendences':attendence,'segment':'worker'})
    if request.method=="POST":
        project=Project.objects.get(id=request.POST.get('project'))
        name=request.POST.get('name')
        one_day_oncome=request.POST.get('one_day_income')
        worker_type=request.POST.get('employee_type')
        worker=Worker.objects.create(name=name,project=project,worker_wages=one_day_oncome,worker_type=worker_type)
        worker.save()
        messages.success(request, 'Worker Added Successfully')
        return redirect('add_worker')    

def Delete_Worker(request,id):
    try:
        worker=Worker.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, 'Worker Deleted Successfully')
        return redirect('add_worker')    
    except:
        return redirect('add_worker')    

def Get_Previous_Worker(request,id):
    if request.is_ajax():
    
        worker=Worker.objects.get(id=id)
        #print(worker.worker_type)
        data={
            'worker_name':worker.name,
            'worker_project':worker.project.title,
            'worker_type':worker.worker_type,
            'worker_wage':worker.worker_wages,
        }
        return JsonResponse(data) 

def Edit_Worker(request):
    worker=Worker.objects.get(id=request.POST.get('worker_id')) 
    
    print(request.POST.get('e_project'),'----------------------')

    if request.POST.get('edit_name'):
        worker.name=request.POST.get('edit_name')
    if request.POST.get('e_project'):
        project=Project.objects.get(id=request.POST.get('e_project'))
        worker.project=project  
    if request.POST.get('e_type'):
        worker.worker_type=request.POST.get('e_type')   
    if request.POST.get('edit_wage'):
        worker.worker_wages=request.POST.get('edit_wage') 
    worker.save()     
    messages.add_message(request, messages.INFO, 'Worker Updated Successfully')
    return redirect('add_worker')



def Add_Attendance(request):
    return render(request,'admin/attendance.html',{'segment':'attendence'})  

import datetime
def View_Project(request,id):  
    project=Project.objects.get(id=id)


    if request.method=="GET": 
       worker=Worker.objects.filter(project=id)
      
       project=Project.objects.get(id=id)
       attendence=Attendence.objects.filter(today=datetime.datetime.now().date(),project__user=request.user,project=id).order_by('-id')
       
    #    a=[]
    #    for w in worker: 
    #        at=Attendence.objects.filter(today=datetime.datetime.now().date(),project__user=request.user,worker=w.id)
    #        a.append(at)
    #        print(at)
    #    z=zip(list(worker),a)          
            
       return render(request,'admin/view_project.html',{'workers':worker,'project':project,'attendences':attendence}) 
    if request.method=='POST':

        worker=Worker.objects.create(project=project,name=request.POST.get('worker_name'),worker_type=request.POST.get('employee_type'),worker_wages=request.POST.get('one_day_income'))

        return redirect('view_project',id=id)   
  

def Mark_Attendance_present(request,id,ids):
    print('++++++++++++++++++++++== ')
    
    if request.method=="GET":
       worker=Worker.objects.get(id=id)
       project=Project.objects.get(id=ids)

       aa=Attendence.objects.filter(project=project,worker=worker) 
       if Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date()).exists():
        #    if request.POST.get('money_paid'):
        #       Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date()).update(money_paid=request.POST.get('money_paid'))
        #       messages.add_message(request, messages.INFO, 'Money Paid Save Successfully')
        #       return redirect('view_project',id=project.id)
        #    else:
                # if Attendence.objects.filter(project=project,worker=worker,attendence=0) or Attendence.objects.filter(project=project,worker=worker,attendence=2):
            messages.add_message(request, messages.INFO, 'Mark Attendence Present')
            print('absent to present')    
            aa.update(project=project,worker=worker,attendence=1)  
            return redirect('view_project',id=project.id)
                # else:
                #   messages.add_message(request, messages.INFO, 'you already mark a present attendance for this worker')
                #   return redirect('view_project',id=project.id) 
       else: 
            Attendence.objects.create(project=project,worker=worker)
            messages.add_message(request, messages.INFO, 'Mark Attendence Present')
            return redirect('view_project',id=project.id)

def Mark_Attendance_Absent(request,id,ids):
    worker=Worker.objects.get(id=id)
    project=Project.objects.get(id=ids)
    aa=Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date())
    if aa:
        messages.add_message(request, messages.INFO, 'Mark Attendence Absent')
        aa.update(project=project,worker=worker,attendence=0)
    else:
        messages.add_message(request, messages.INFO, 'Mark Attendence Absentt')
        Attendence.objects.create(project=project,worker=worker,attendence=0)
    return redirect('view_project',id=project.id)


def Mark_Short_Day(request,id,ids):
    worker=Worker.objects.get(id=id)
    project=Project.objects.get(id=ids)
    aa=Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date())
    if aa:
        messages.add_message(request, messages.INFO, 'Mark Attendence Shorty Day')
        aa.update(project=project,worker=worker,attendence=2)
    else:
        messages.add_message(request, messages.INFO, 'Mark Attendence Absentt')
        Attendence.objects.create(project=project,worker=worker,attendence=2)
    return redirect('view_project',id=project.id)


def Already_Paid(request,id,ids):
    worker=Worker.objects.get(id=id)
    project=Project.objects.get(id=ids)
    aa=Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date())
    if request.POST.get('money_paid'):
              Attendence.objects.filter(project=project,worker=worker,today=datetime.datetime.now().date()).update(money_paid=request.POST.get('money_paid'))
              messages.add_message(request, messages.INFO, 'Money Paid Save Successfully')
              return redirect('view_project',id=project.id)
    return redirect('view_project',id=project.id)




def View_Attendence(request,id,ids):
    attendence=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids).order_by('-id')
    w_w=Worker.objects.get(id=id).worker_wages
    a_c=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids,attendence='1').count()
    try:
       a_s_d_c=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids,attendence='2').count()
       w_s_d_w=round(Worker.objects.get(id=id).worker_wages/2)*a_s_d_c

    except:
        pass  

    total_income=w_w*a_c
    t_income_Include_half_day=total_income+w_s_d_w

    already_paid=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids)
    already_paid=sum(x.money_paid for x in already_paid if x.money_paid is not None)

    amount_to_pay=t_income_Include_half_day-already_paid

    months = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July',
          '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}    
    return render(request,'admin/view_attendence.html',{'attendences':attendence,'total_income':t_income_Include_half_day,'already_paid':already_paid,'amount_to_pay':amount_to_pay,'months':months,'worker_id':id,'project_id':ids}) 


def search_by_month(request,id,ids):

    w_w=Worker.objects.get(id=id).worker_wages
    a_c=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids,attendence='1').count()
    total_income=w_w*a_c

    already_paid=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids)
    already_paid=sum(x.money_paid for x in already_paid if x.money_paid is not None)

    amount_to_pay=total_income-already_paid

    # for i in already_paid:
    #     if i.money_paid is not None:
    #       print(i.money_paid)
    
    attendence=Attendence.objects.filter(created_at__month=datetime.datetime.now().month,worker=id,project=ids).order_by('-id')
    if request.GET.get('months'):
        w_w=Worker.objects.get(id=id).worker_wages
        a_c=Attendence.objects.filter(created_at__month=request.GET.get('months'),worker=id,project=ids,attendence='1').count()
        total_income=w_w*a_c
        attendence=Attendence.objects.filter(created_at__month=request.GET.get('months'),worker=id,project=ids).order_by('-id')
        already_paid=Attendence.objects.filter(created_at__month=request.GET.get('months'),worker=id,project=ids,)
        already_paid=sum(x.money_paid for x in already_paid if x.money_paid is not None)

        amount_to_pay=total_income-already_paid
        
    months = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July',
          '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}    
    return render(request,'admin/view_attendence.html',{'attendences':attendence,'total_income':total_income,'already_paid':already_paid,'amount_to_pay':amount_to_pay,'months':months,'worker_id':id,'project_id':ids}) 


def Add_Material(request):
    msg = None
    success = False

    if request.method == "GET":
        form = MaterialForm()
        material=Material.objects.all().order_by('-id')
        return render(request, 'admin/material.html', {"form": form,'material':material,'segment':'material'})   


    if request.method=='POST':
        fm=MaterialForm(request.POST)
        if fm.is_valid():
             m_t=fm.cleaned_data['material_type']
             m_m_t=fm.cleaned_data['manual_material_type']
             figure=fm.cleaned_data['figure']
             unit=fm.cleaned_data['unit']
             price_per_item=fm.cleaned_data['price_per_item']
            #  money_paid=fm.cleaned_data['money_paid']
             purpose=fm.cleaned_data['purpose']
             size=fm.cleaned_data['size']
             project=fm.cleaned_data['project']
             retailer=fm.cleaned_data['retailer']
             mat=Material(retailer=retailer,material_type=m_t,manual_material_type=m_m_t,figure=figure,unit=unit,price_per_item=price_per_item,size=size,purpose=purpose,project=project)
             mat.save()
            #  fm = MaterialForm()  
             messages.add_message(request, messages.INFO, 'Material added successfully')
             return redirect('add_material')  

def Get_Previous_Material(request,id):
    material=Material.objects.get(id=id)
    # print(material.retailer.name)
    data={
        'retailer':material.retailer.name,
        'project':material.project.title,
        'material_type':material.material_type,
        'manual_material_type':material.manual_material_type,
        'quantity':material.quantity,
        'figure':material.figure,
        'unit':material.unit,
        'size':material.size,
        'purpose':material.purpose,
        'price_per_item':material.price_per_item,
        'money_paid':material.money_paid,
        'total_money':material.total_price,
        # 'money_to_pay':material.total_price-material.money_paid,
    }
    return JsonResponse(data)      

def Edit_Material(request):
    material=Material.objects.get(id=request.POST.get('material_id'))
    p_p_i=material.price_per_item
    unit=material.unit
    print(unit)
    print(p_p_i)
    if request.POST.get('edit_retailer'):
        material.retailer=Retailer.objects.get(id=request.POST.get('edit_retailer'))
    if request.POST.get('e_id_material_type'):
        material.material_type=request.POST.get('e_id_material_type')   
    if request.POST.get('e_figure'):
        material.figure=request.POST.get('e_figure')
        
    if request.POST.get('e_id_unit'):
        material.unit=request.POST.get('e_id_unit')   
    if request.POST.get('e_id_purpose'):
        material.purpose=request.POST.get('e_id_purpose') 
    if request.POST.get('e_id_size'):
        material.size=request.POST.get('e_id_size')     
    if request.POST.get('e_id_price_per_item'):
        material.price_per_item=request.POST.get('e_id_price_per_item')  
    # if request.POST.get('e_id_money_paid'):
    #     material.money_paid=request.POST.get('e_id_money_paid')             
    material.save()    
    messages.add_message(request, messages.INFO, 'Project Updated Successfully')

    return redirect('show_material',id=request.POST.get('project_id'))          

def Add_Retialer(request):
    if request.method=="GET":
        print('+++++++++++++++++++++++++++++++')
        print(request.user)
        retailer=Retailer.objects.filter(user=request.user).order_by('-id')
        
        rr=[]
        tm=[]
        mp=[]
        atp=[]
        ff=[]

        for i in retailer:
    
           r=Retailer.objects.get(id=i.id)
           rr.append(r)
    
           t_m=sum(x.total_price for x in Material.objects.filter(retailer=i) if x.total_price is not None)
           tm.append(t_m)

           m_p=sum(x.money_paid for x in Material.objects.filter(retailer=i) if x.money_paid is not None)
           mp.append(m_p)  

           m_t_p=t_m-m_p
           atp.append(m_t_p)

           Retailer.objects.filter(id=i.id).update(total_ammount=t_m,money_paid=m_p,amount_to_pay=m_t_p)

        zipped=zip(rr,tm,mp,atp)   

        ff.append(list(zipped))  
        data=ff  

        return render(request,'admin/add_retailer.html',{'segment':'retailer','retailer':retailer,'data':data})  
    if request.method=="POST":
        print('------------------------------')
        retailer=Retailer.objects.create(user=request.user,name=request.POST.get('retailer_name'),phone=request.POST.get('contact'),shop_name=request.POST.get('shop'),vehicle_number=request.POST.get('number'))
        return redirect('add_retailer')


def Get_Previous_Retailer(request,id):
    if request.is_ajax():
        print(id)
        retailer=Retailer.objects.get(id=id)
        data={
            'name':retailer.name,
            'contact':str(retailer.phone),
            'shop_name':retailer.shop_name,
            'vehicle_number':retailer.vehicle_number,
            'total_ammount':retailer.total_ammount,
            'money_paid':retailer.money_paid,
            'amount_to_pay':retailer.amount_to_pay,
        }
        return JsonResponse(data) 

def Delete_Retailer(request,id):
    retailer=Retailer.objects.get(id=id)
    retailer.delete()
    return redirect('add_retailer')

def Edit_Retailer(request):
    retailer=Retailer.objects.get(id=request.POST.get('retailer_id'))

    if request.POST.get('e_retailer_name'):
        retailer.name=request.POST.get('e_retailer_name')

    if request.POST.get('e_contact'):
        retailer.phone=request.POST.get('e_contact')
        
    if request.POST.get('e_shop'):
        retailer.shop=request.POST.get('e_shop')  

    if request.POST.get('e_number'):
        retailer.vehicle_number=request.POST.get('e_number')         
    retailer.save()
    return redirect('add_retailer')


def View_Retialer(request,id):
    print('========================')
    material=Material.objects.filter(retailer=id)
    t_p=sum(x.total_price for x in Material.objects.filter(retailer=id) if x.total_price is not None)
    m_p=sum(x.money_paid for x in Material.objects.filter(retailer=id) if x.money_paid is not None)
    m_t_p=t_p-m_p 

    try:
        for i in material:
             if i.total_price==i.money_paid:
                 i.paid=True
             else:
                 i.paid=False    
             i.save()
    except:
        pass         

    # a=[y.paid==True for y in material if y.total_price==y.money_paid]
    # print(a)
    # a.save

    # a=y.paid for y in material if y.total_price==y.money_paid
    # a.save()
    return render(request,'admin/view_retailer.html',{'retailer_id':id,'material':material,'total_price':t_p,'money_paid':m_p,'money_to_pay':m_t_p})

#pay money to each product in retailer module.
def Pay_Money(request,id):
    try:
        print(request.POST.get('p_pay_ammount'))
    
        #kal meko handel krna h ki agr me material edit krta hu project m jaake to meko retailer mai usko handel krna h ki kese payment kru.
        # mm=Material.objects.get(id=request.POST.get('p_material_id')).money_paid
        # print(mm)
        m_a_p=Material.objects.get(id=request.POST.get('p_material_id')).money_paid
        print(m_a_p,'9999999999999999')
    
        if m_a_p is not None:
            aaa=m_a_p+int(request.POST.get('p_pay_ammount'))
            m=Material.objects.filter(id=request.POST.get('p_material_id')).update(money_paid=aaa)
        else:
            m=Material.objects.filter(id=request.POST.get('p_material_id')).update(money_paid=request.POST.get('p_pay_ammount'))
    except:
        pass
    return redirect('view_retailer',id=id)

#pay retailer whole ammount
def Pay_Retialer_Money(request):
    try:
        money_paid=Retailer.objects.get(id=request.POST.get('p_retailer_id')).money_paid
        print(money_paid,'============')
    
        total_ammount_paid=money_paid+int(request.POST.get('p_pay_ammount'))
        print(total_ammount_paid)
    
        mm=Material.objects.filter(retailer=request.POST.get('p_retailer_id'))
    
        for i in mm:
            Material.objects.filter(id=i.id).update(money_paid=i.total_price)
    except:
        pass       
    return redirect('add_retailer')
    # return redirect('add_retailer')

    
def Pay_Money_project(request,id):
    
    print(id,'---------------------')
    print(request.POST.get('p_pay_ammount'))
    try:
        m_a_p=Material.objects.get(id=request.POST.get('p_material_id')).money_paid
        print(m_a_p)
    
        if m_a_p is not None:
            aaa=m_a_p+int(request.POST.get('p_pay_ammount'))
            m=Material.objects.filter(id=request.POST.get('p_material_id')).update(money_paid=aaa)
        else:
            m=Material.objects.filter(id=request.POST.get('p_material_id')).update(money_paid=request.POST.get('p_pay_ammount'))
    except:
        pass        
    return redirect('show_material',id=id)

    



    