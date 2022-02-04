from django.contrib import admin
from django.urls import include, path
from .views import workspace_views as wv, board_views as bv

urlpatterns = [
  path('', wv.fetch_all_workspaces, name='workspaces'),
  path('add', wv.add_workspace, name='add-workspace'),
  path('deactivate/', wv.deactivate_workspace, name='deactivate-workspace'),
  path('edit/<str:encrypted_workspace_id>', wv.edit_workspace, name='edit-workspace'),
  path('boards/<str:encrypted_workspace_id>', bv.fetch_all_boards, name='boards'),
  path('boards/add/<str:encrypted_workspace_id>/<str:workspace_title>', bv.add_board, name='add-board'),
  path('boards/edit/<str:encrypted_workspace_id>/<int:board_id>', bv.edit_board_title, name='edit-board'),
  path('cards/add/<str:encrypted_board_id>', bv.edit_board_title, name='add-card')
]

