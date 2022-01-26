from django import forms
from .models import User
from django.core.validators import EmailValidator

attrs = {
  "class": "form-control form-control-sm"
}
class RegisterForm(forms.ModelForm):
  confirmation_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs), required=True)
  password = forms.CharField(widget=forms.PasswordInput(attrs=attrs), required=True)
  username = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
  first_name = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
  last_name = forms.CharField(widget=forms.TextInput(attrs=attrs), required=True)
  email = forms.EmailField(widget=forms.EmailInput(attrs=attrs), validators=[EmailValidator], required=True)

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
  
  def clean(self):
    password = self.cleaned_data['password']
    confirmation_password = self.cleaned_data['confirmation_password']
    if (password != confirmation_password):
      raise forms.ValidationError("password and confirmation password do not match")
    return super().clean()
  
  def save(self):
    new_user: User = User(
      first_name = self.cleaned_data['first_name'],
      last_name = self.cleaned_data['last_name'],
      username = self.cleaned_data['username'],
      email = self.cleaned_data['email']
    )
    new_user.set_password(self.cleaned_data['password'])
    
    return new_user.save(True)
    
  
class LoginForm(forms.Form):
  username_or_email = forms.CharField(widget=forms.TextInput(attrs=attrs))
  password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))