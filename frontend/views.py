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

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from paywix.payu import Payu
from django.http import JsonResponse
from paywix.payu import Payu
from django.views.decorators.csrf import csrf_exempt
payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request,'admin/home.html')
    return render(request,'admin/home.html')


def Payu(request):
        print('2222222222222')
        print(merchant_salt,'3333333333333333333')

    # if request.method == 'POST':
        # Making Checkout form into dictionary
        # data = {k: v[0] for k, v in dict(request.POST).items()}
        # data.pop('csrfmiddlewaretoken')
        # The dictionary data  should be contains following details
        data = { 'amount': '10', 
            'firstname': 'renjith', 
            'email': 'renjithsraj@gmail.com',
            'phone': '9746272610', 'productinfo': 'test', 
            'lastname': 'test', 'address1': 'test', 
            'address2': 'test', 'city': 'test', 
            'state': 'test', 'country': 'test', 
            'zipcode': 'tes', 'udf1': '', 
            'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
        }
        import uuid
        lowercase_str = uuid.uuid4().hex

        print(lowercase_str)

        txnid = "Create your transaction id"
        data.update({"txnid": f"{lowercase_str}"})
        payu_data = payu.transaction(**data)
        print(payu_data)
        return render(request, 'admin/payu.html', {"posted": payu_data})


@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)        

# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)    