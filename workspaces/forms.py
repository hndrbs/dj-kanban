from django import forms
from .models import Board, Card, Workspace


class WorkspaceForm(forms.ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
  desc = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-control-sm"}))
  class Meta:
    model = Workspace
    fields = ['title', 'desc']

class BoardForm(forms.ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
  class Meta:
    model = Board
    fields = ['title']

class CardForm(forms.ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"})) 
  target_date = forms.CharField(widget=forms.DateInput(attrs={
    'type': 'date',
    'class': 'form-control form-control-sm'
  }))
  class Meta:
    model = Card
    fields = ['title', 'target_date']