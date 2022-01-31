from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
  path('', fetch_all_workspaces, name='workspaces'),
  path('add', add_workspace, name='add-workspace'),
  path('del/<str:b64_id>', deactivate_workspace, name='deactivate-workspace')
]

