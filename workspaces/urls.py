from django.urls import path
from .views import (
  workspace_views as wv,
  board_views as bv,
  card_views as cv
)

urlpatterns = [
  path('', wv.fetch_all_workspaces, name='workspaces'),
  path('add', wv.add_workspace, name='add-workspace'),
  path('deactivate/', wv.deactivate_workspace, name='deactivate-workspace'),
  path('edit/<str:encrypted_workspace_id>', wv.edit_workspace, name='edit-workspace'),
  path('boards/delete', bv.delete_board, name='delete-board'),
  path('boards/add/<str:encrypted_workspace_id>', bv.add_board, name='add-board'),
  path('boards/edit/<str:encrypted_workspace_id>/<str:encrypted_board_id>', bv.edit_board_title, name='edit-board'),
  path('boards/<str:encrypted_workspace_id>', bv.fetch_all_boards, name='boards'),
  path('cards/add/<str:encrypted_board_id>', cv.add_card, name='add-card'),
  path('cards/edit/<str:encrypted_workspace_id>/<str:encrypted_board_id>/<str:encrypted_card_id>', cv.edit_card, name='edit-card'),
  path('cards/delete/<str:encrypted_workspace_id>', cv.delete_card, name='delete-card'),
  path('cards/move', cv.move_card_to_another_board, name='move-card')
]

