from django import forms
from .models import Board, Workspace


class WorkspaceForm(forms.ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
  desc = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-control-sm"}))
  class Meta:
    model = Workspace
    fields = ['title', 'desc']

class BoardForm(forms.ModelForm):
  class Meta:
    model = Board
    fields = ['title']