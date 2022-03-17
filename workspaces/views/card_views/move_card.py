from workspaces.models import Workspace
from .importer import *

@login_required
@require_http_methods(['POST'])
def move_card_to_another_board(request: HttpRequest) -> HttpResponse:
  try:
    data = request.POST
    board_id_from = get_model_id(data.get('board_from'))
    board_id_to = get_model_id(data.get('board_to'))
    card_id = get_model_id(data.get('card_id'))
    workspace_id = get_model_id(data.get('workspace_id'))

    current_card = Card.objects.filter(Q(id=card_id)& Q(board_id=board_id_from))
    is_card_exist_in_this_board = current_card.exists()
    
    is_next_board_exist = Board.objects\
                            .filter(Q(id=board_id_to) & Q(workspace_id=workspace_id)).exists()
    if is_card_exist_in_this_board and is_next_board_exist:
      card = current_card.first()
      card.board_id = board_id_to
      card.save()
      messages.success(request, "Successfully to move a card")
      board = Board.objects.filter(id=board_id_to).first()
      workspace = Workspace.objects.filter(id=workspace_id).first()
      context = {
        "board": board,
        "workspace": workspace,
        "card": card,
        "partial": True
      }

      return djrender(request, "components/card.html", context)
    
    messages.warning(request, Const.INVALID_MOVE_CARD)

  except Exception as err:
    exception_message_dispatcher(request, err)
  
  return djrender(request, "messages.html")
  