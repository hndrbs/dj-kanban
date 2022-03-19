from django.urls import path
from . import views

urlpatterns = [
  path('delete', views.delete_card, name='delete-card'),
  path('move', views.move_card_to_another_board, name='move-card'),
  path('add/<str:encrypted_board_id>', views.add_card, name='add-card'),
  path('last/<str:encrypted_board_id>', views.fetch_last_created_card, name='last-card'),
  path('one/<str:encrypted_board_id>/<str:encrypted_card_id>', views.fetch_one_card, name='one-card'),
  path('edit/<str:encrypted_board_id>/<str:encrypted_card_id>', views.edit_card, name='edit-card'),
  path('<str:encrypted_board_id>', views.fetch_cards_by_board_id, name='cards-by-board-id'),
]