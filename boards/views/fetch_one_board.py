from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_one_board(request: HttpRequest, encrypted_workspace_id: str, encrypted_board_id:str) -> HttpResponse:
  workspace_id = get_model_id(encrypted_workspace_id)
  id = get_model_id(encrypted_board_id)
  board = Board.objects.filter(Q(id=id) & Q(workspace_id=workspace_id)).first()
  virtual_workspace = Workspace(id=workspace_id)
  context = {
    "board": board,
    "workspace": virtual_workspace,
    "partial": True
  }
  
  messages.success(request, "successfully edit a board")
  # for board, only title that could be edited
  return djrender(request, "components/board_header.html", context)