
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Material,Retailer


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['retailer','project','material_type','manual_material_type','figure','unit','purpose','size','price_per_item']
        widgets={
          'retailer':forms.Select(attrs={'class':'form-control'}),
          'material_type':forms.Select(attrs={'class':'form-control'}),
          'manual_material_type':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Material Type Manually'}),
          'project':forms.Select(attrs={'class':'form-control'}),
        #   'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
          'figure': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Number of Items'}),
          'unit': forms.Select(attrs={'class': 'form-control'}),
          'purpose': forms.Textarea(attrs={'class': 'form-control','rows':2}),
          'price_per_item': forms.TextInput(attrs={'class': 'form-control', }),
          'size': forms.TextInput(attrs={'class': 'form-control'}),
        #   'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
        #   'money_paid': forms.NumberInput(attrs={'class': 'form-control'})
      }
   
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['retailer'].empty_label = "Choose Retailer"  
        self.fields['project'].empty_label = "Choose Project"      
     

class ShowMaterialForm(forms.ModelForm):
    # add_material_type_manualy=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Add Material Type Manually','required':'False'}))
    # retailer=forms.ModelChoiceField(queryset=Retailer.objects.all(),empty_label="Choose Retailer")
      
    class Meta:
        model = Material
        fields = ['retailer','material_type','manual_material_type','figure','unit','purpose','size','price_per_item']
        widgets={
          'retailer':forms.Select(attrs={'class':'form-control'}),
          'material_type':forms.Select(attrs={'class':'form-control'}),
          'manual_material_type':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Material Type Manually'}),
        #   'project':forms.Select(attrs={'class':'form-control'}),
        #   'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
          'figure': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Number of Items'}),
          'unit': forms.Select(attrs={'class': 'form-control'}),
          'purpose': forms.Textarea(attrs={'class': 'form-control','rows':2}),
          'price_per_item': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Rs'}),
          'size': forms.TextInput(attrs={'class': 'form-control'}),
        #   'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
        #   'money_paid': forms.NumberInput(attrs={'class': 'form-control'})
      }

    def __init__(self, *args, **kwargs):
        super(ShowMaterialForm, self).__init__(*args, **kwargs)
        self.fields['retailer'].empty_label = "Choose Retailer"      
     
