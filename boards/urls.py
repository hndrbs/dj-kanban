from django.urls import path
from . import views


urlpatterns = [
  path('delete', views.delete_board, name='delete-board'),
  path('lastcreated/<str:encrypted_workspace_id>', views.fetch_last_created_board, name='last-board'),
  path('refresh/<str:encrypted_board_id>', views.refresh_board, name='refresh-board'),
  path('add/<str:encrypted_workspace_id>', views.add_board, name='add-board'),
  path('one/<str:encrypted_workspace_id>/<str:encrypted_board_id>', views.fetch_one_board, name='one-board'),
  path('edit/<str:encrypted_workspace_id>/<str:encrypted_board_id>', views.edit_board_title, name='edit-board'),
  path('<str:encrypted_workspace_id>', views.fetch_all_boards, name='boards'),
]