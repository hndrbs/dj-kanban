from django.urls import path
from . import views

urlpatterns = [
  path('add', views.add_workspace, name='add-workspace'),
  path('delete', views.delete_workspace, name='delete-workspace'),
  path('lastcreated', views.fetch_last_created_workspace, name='last-workspace'),
  path('one/<str:encrypted_workspace_id>', views.fetch_one_workspace, name='one-workspace'),
  path('edit/<str:encrypted_workspace_id>', views.edit_workspace, name='edit-workspace'),
  path('', views.fetch_all_workspaces, name='workspaces'),
]

