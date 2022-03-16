from workspaces.models import Workspace
from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_one_card(
  request: HttpRequest,
  encrypted_workspace_id: str, 
  encrypted_board_id: str,
  encrypted_card_id: str
) -> HttpResponse:

  workspace_id = get_model_id(encrypted_workspace_id)
  board_id = get_model_id(encrypted_board_id)
  id = get_model_id(encrypted_card_id)
  card = Card.objects.filter(board_id=board_id).filter(id=id).first()
  context = {
    "card": card,
    "partial": True,
    "board": Board(id=board_id),
    "workspace": Workspace(id=workspace_id),
  }
  
  messages.success(request, "successfully edit a card")

  return djrender(request, "components/card.html", context)