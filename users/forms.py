from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
  attrs = {
      "class": "form-control form-control-sm"
    }
  confirmation_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
  password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
  username = forms.CharField(widget=forms.TextInput(attrs=attrs))
  first_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
  last_name = forms.CharField(widget=forms.TextInput(attrs=attrs))
  email = forms.EmailField(widget=forms.EmailInput(attrs=attrs))

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
  