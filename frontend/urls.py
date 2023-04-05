from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'frontend'

urlpatterns = [
    path('', frontend, name='frontend'),
    path('dance/', Dance, name='dance'),
    path('about/', About, name='about'),
    path('classes/', Classes, name='classes'),
    path('contact/', Contacts, name='contact'),
    path('about_us/', Aboutt, name='about_us'),

    path('payu/', Payu, name='payu'),
    path('payu/success/', payu_success, name='payu_success'),
    path('payu/faliour/', payu_failure, name='payu_failure'),    

]
