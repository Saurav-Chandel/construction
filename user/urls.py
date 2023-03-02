from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'user'

urlpatterns = [
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', index, name='index'),
    path('profile/', Profile, name='profile'),
    path('add-project/', Add_Project, name='add_project'),
    path('delete-project/<int:id>/', Delete_Project, name='delete_project'),
    path('edit-project/', Edit_Project, name='edit_project'),
    path('get-privous-project/<int:id>/', Get_Previous_Project, name='get_previous_project'),
    path('view_project/<int:id>/', View_Project, name='view_project'),
    
    path('add-worker/', Add_Worker, name='add_worker'),
    path('delete-worker/<int:id>/', Delete_Worker, name='delete_worker'),
    path('get-privous-worker/<int:id>/', Get_Previous_Worker, name='get-privous-worker '),
    path('edit-worker/', Edit_Worker, name='edit_worker'),

    path('add-attendance/', Add_Attendance, name='add_attendance'),
    path('mark-attendance-present/<int:id>/<int:ids>/', Mark_Attendance_present, name='mark_attendance_present'),
    path('mark-attendance-absent/<int:id>/<int:ids>/', Mark_Attendance_Absent, name='mark_attendance_absent'),
    path('mark-short-attendence/<int:id>/<int:ids>/', Mark_Short_Day, name='mark_short_attendance'),
    path('already_paid/<int:id>/<int:ids>/', Already_Paid, name='already_paid'),

    path('view_attenence/<int:id>/<int:ids>/', View_Attendence, name='view_attendence'),
    path('search_by_month/<int:id>/<int:ids>/', search_by_month, name='search_by_month'),

    path('add-material/', Add_Material, name='add_material'),
    path('edit-material/', Edit_Material, name='edit_material'),
    path('show-material/<int:id>/', Show_Material, name='show_material'),
    path('pay-money-project/<int:id>/', Pay_Money_project, name='pay_money_project'),
    path('get-previous-material/<int:id>/', Get_Previous_Material, name='get_previous_material'),

    path('add-retailer/',Add_Retialer, name='add_retailer'),
    path('get-previous-retailer/<int:id>/',Get_Previous_Retailer, name='get_previous_retailer'),
    path('delete-retailer/<int:id>/',Delete_Retailer, name='delete_retailer'),
    path('edit-retailer/',Edit_Retailer, name='edit_retailer'),
    path('view-retailer/<int:id>/',View_Retialer, name='view_retailer'),
    path('pay_money/<int:id>/',Pay_Money, name='pay_money'),
    path('pay-Retailer-money/',Pay_Retialer_Money, name='pay_Retailer_money'),

    #contact
    path('contact/',ContactListing, name='contact'),
    path('delete-contact/<int:id>/',DeleteContact, name='delete_contact'),
    path('dashboard/',DashboardData, name='chart_data'),

    #dance
    path('classes/',Add_Classes, name='classes'),
    path('delete-class/',Delete_Class, name='delete_class'),

]