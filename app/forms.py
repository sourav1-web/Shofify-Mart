from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegForm(UserCreationForm):
  password1=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
  password2=forms.CharField(label='password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
  email=forms.CharField(label='Email', required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']
    labels={'email':'Email'}
    widgets={'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
  username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
  password=UsernameField(label=_('password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class PwdchangeForm(PasswordChangeForm):
  old_password=forms.CharField(label=_("Old_password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
  new_password1=forms.CharField(label=_("new_password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())       
  new_password2=forms.CharField(label=_("confirm_password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'}))     

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure that all fields are required
        for field in self.fields.values():
            field.required = True



    