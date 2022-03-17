from .importer import *

@login_required
@require_http_methods(["GET"])
def refresh_board (request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  try:
    board_id = get_model_id(encrypted_board_id)
    board = Board.objects.filter(id=board_id).first()
    cards = Card.objects.filter(board=board).select_related('board')
    
    context = {
      'board': board,
      'cards': cards,
    }
    
    return djrender(request, 'components/board.html', context)
  
  except Workspace.DoesNotExist:
    messages.warning(request, Const.NOT_FOUND_BOARD)
  
  except Exception as err:
    exception_message_dispatcher(request, err)
  
  return redirect(urls.reverse('workspaces'))