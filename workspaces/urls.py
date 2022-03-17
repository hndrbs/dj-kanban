from django.urls import path
from .views import (
  workspace_views as wv,
  board_views as bv,
  card_views as cv
)

urlpatterns = [
  path('add', wv.add_workspace, name='add-workspace'),
  path('delete', wv.delete_workspace, name='delete-workspace'),
  path('lastcreated', wv.fetch_last_created_workspace, name='last-workspace'),
  path('one/<str:encrypted_workspace_id>', wv.fetch_one_workspace, name='one-workspace'),
  path('edit/<str:encrypted_workspace_id>', wv.edit_workspace, name='edit-workspace'),
  path('', wv.fetch_all_workspaces, name='workspaces'),


  path('boards/delete', bv.delete_board, name='delete-board'),
  path('boards/lastcreated/<str:encrypted_workspace_id>', bv.fetch_last_created_board, name='last-board'),
  path('boards/one/<str:encrypted_workspace_id>/<str:encrypted_board_id>', bv.fetch_one_board, name='one-board'),
  path('boards/add/<str:encrypted_workspace_id>', bv.add_board, name='add-board'),
  path('boards/edit/<str:encrypted_workspace_id>/<str:encrypted_board_id>', bv.edit_board_title, name='edit-board'),
  path('boards/<str:encrypted_workspace_id>', bv.fetch_all_boards, name='boards'),


  path('cards/delete', cv.delete_card, name='delete-card'),
  path('cards/move', cv.move_card_to_another_board, name='move-card'),
  path('cards/add/<str:encrypted_board_id>', cv.add_card, name='add-card'),
  path('cards/last/<str:encrypted_board_id>', cv.fetch_last_created_card, name='last-card'),
  path('cards/one/<str:encrypted_workspace_id>/<str:encrypted_board_id>/<str:encrypted_card_id>', cv.fetch_one_card, name='one-card'),
  path('cards/edit/<str:encrypted_board_id>/<str:encrypted_card_id>', cv.edit_card, name='edit-card'),
]

