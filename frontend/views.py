from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from user.models import *
import datetime

# Create your views here.

def frontend(request):
    if request.method=="GET":
        c = AddClasses.objects.all().order_by('-created_at')
        about_us=AboutUs.objects.all()
        print(about_us.values())
        return render(request,'frontend/index.html',{'classes':c,'about_us':about_us})

    if request.method=="POST":
        Contact.objects.create(f_name=request.POST.get('f_name'),
                            l_name=request.POST.get('l_name'),
                            email=request.POST.get('email'),
                            phone=request.POST.get('phone'),
                            message=request.POST.get('message'),
                            )
        messages.add_message(request, messages.INFO, 'Thank you for filling out your information!')
        return redirect('frontend:frontend')        

    return render(request,'frontend/index.html')

def Dance(request):
    return render(request,'frontend/dance.html')    

def About(request):
    return render(request,'frontend/about.html')    

def Classes(request):
    c = AddClasses.objects.all().order_by('-created_at')
    return render(request,'frontend/classes.html',{'classes':c}) 

def Contacts(request):
    if request.method=="GET":
        try:
          contact=Contact.objects.all()
          return render(request,'frontend/contact.html',{'contact':contact})
        except:
          return render(request,'frontend/contact.html')
          
    if request.method=="POST":
        Contact.objects.create(f_name=request.POST.get('f_name'),
                            l_name=request.POST.get('l_name'),
                            email=request.POST.get('email'),
                            phone=request.POST.get('phone'),
                            message=request.POST.get('message'),
                           )
        messages.add_message(request, messages.INFO, 'Thank you for filling out your information!')
        return redirect('frontend:frontend')        
           

def Aboutt(request):
    print('ddddddddddddddddd')
    print(request.POST.get('title'))
    print(request.POST.get('description'),)
    print(request.FILES.get('video_file'))
    if request.method=='POST':
        AboutUs.objects.create(title=request.POST.get('title'),
                            description=request.POST.get('description'),
                            vedio_file=request.FILES.get('video_file'))
    
        messages.add_message(request, messages.INFO, 'About Us Added successfuly')
        return redirect('user:classes')                      

