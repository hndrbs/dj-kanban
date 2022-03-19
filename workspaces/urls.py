from django.urls import path
from .views import (
  workspace_views as wv,
  card_views as cv
)

urlpatterns = [
  path('add', wv.add_workspace, name='add-workspace'),
  path('delete', wv.delete_workspace, name='delete-workspace'),
  path('lastcreated', wv.fetch_last_created_workspace, name='last-workspace'),
  path('one/<str:encrypted_workspace_id>', wv.fetch_one_workspace, name='one-workspace'),
  path('edit/<str:encrypted_workspace_id>', wv.edit_workspace, name='edit-workspace'),
  path('', wv.fetch_all_workspaces, name='workspaces'),

  path('cards/delete', cv.delete_card, name='delete-card'),
  path('cards/move', cv.move_card_to_another_board, name='move-card'),
  path('cards/add/<str:encrypted_board_id>', cv.add_card, name='add-card'),
  path('cards/last/<str:encrypted_board_id>', cv.fetch_last_created_card, name='last-card'),
  path('cards/one/<str:encrypted_board_id>/<str:encrypted_card_id>', cv.fetch_one_card, name='one-card'),
  path('cards/edit/<str:encrypted_board_id>/<str:encrypted_card_id>', cv.edit_card, name='edit-card'),
  path('cards/<str:encrypted_board_id>', cv.fetch_cards_by_board_id, name='cards-by-board-id'),
]

