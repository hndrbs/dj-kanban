from .importer import *

@login_required
@require_http_methods(['POST'])
def delete_board(request: HttpRequest) -> HttpResponse:
  try:
    encrypted_board_id = request.POST.get('board_id')
    encrypted_workspace_id = request.POST.get('workspace_id')

    board_id = get_model_id(encrypted_board_id)
    workspace_id = get_model_id(encrypted_workspace_id)
    
    board = Board.objects.filter(Q(id=board_id) & Q(workspace_id=workspace_id))

    if board.exists():
      board.delete()
      return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))
    
    messages.warning(request, Const.NOT_FOUND_BOARD)
  
  except Exception as err:
    exception_message_dispatcher(request, err)
  
  return redirect(urls.reverse('workspaces'))