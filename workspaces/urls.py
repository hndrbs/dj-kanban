from django.contrib import admin
from django.urls import include, path
from .views import fetch_all_workspaces

urlpatterns = [
  path('', fetch_all_workspaces, name='workspaces'),
]

