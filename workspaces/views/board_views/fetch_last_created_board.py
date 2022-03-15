from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_last_created_board(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  workspace_id = get_model_id(encrypted_workspace_id)
  board = Board.objects.filter(workspace_id=workspace_id).order_by('-created_at').first()
  context = {
    "board": board,
    "partial": True
  }
  
  messages.success(request, "successfully save a new board")

  return djrender(request, "components/board.html", context)