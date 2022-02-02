from django.contrib import admin
from django.urls import include, path
from .views import workspace_views as wv

urlpatterns = [
  path('', wv.fetch_all_workspaces, name='workspaces'),
  path('add', wv.add_workspace, name='add-workspace'),
  path('del/<str:b64_id>', wv.deactivate_workspace, name='deactivate-workspace'),
  path('edit/<str:b64_id>', wv.edit_workspace, name='edit-workspace')
]

