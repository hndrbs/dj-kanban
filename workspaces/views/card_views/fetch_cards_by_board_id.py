from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_cards_by_board_id(request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  board_id = get_model_id(encrypted_board_id)
  cards = Card.objects.filter(board_id=board_id).order_by('-updated_at')
  board = Board.objects.filter(id=board_id).first()
  context = {
    "cards": cards,
    "board": board
  }
  
  return djrender(request, "components/cards.html", context)