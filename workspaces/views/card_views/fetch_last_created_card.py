from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_last_created_card(request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  board_id = get_model_id(encrypted_board_id)
  card = Card.objects.filter(board_id=board_id).order_by('-created_at').first()
  context = {
    "card": card,
    "partial": True,
    "board": Board(id=board_id)
  }
  
  messages.success(request, "successfully save a new card")

  return djrender(request, "components/card.html", context)