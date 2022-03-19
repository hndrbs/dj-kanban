from workspaces.models import Workspace
from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_one_card(
  request: HttpRequest,
  encrypted_board_id: str,
  encrypted_card_id: str
) -> HttpResponse:

  board_id = get_model_id(encrypted_board_id)
  id = get_model_id(encrypted_card_id)
  card = Card.objects.filter(board_id=board_id).filter(id=id).first()
  board = Board.objects.filter(id=board_id).first()
  workspace = Workspace.objects.filter(id=board.workspace_id)
  context = {
    "card": card,
    "partial": True,
    "board": board,
    "workspace": workspace,
  }
  
  messages.success(request, "successfully edit a card")

  return djrender(request, "components/card.html", context)