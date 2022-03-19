from .importer import *

@login_required
@require_http_methods(["GET"])
def fetch_all_boards(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  try:
    workspace_id = get_model_id(encrypted_workspace_id)
    workspace = Workspace.objects.get(id=workspace_id)
    boards = Board.objects.filter(workspace=workspace)
    cards = Card.objects.filter(board__in=boards).select_related('board')
    
    context = {
      'boards': boards,
      'cards': cards,
      'workspace': workspace
    }
    
    return render(request, 'boards.html', context)
  
  except Workspace.DoesNotExist:
    messages.warning(request, Const.NOT_FOUND_BOARD)
  
  except Exception as err:
    exception_message_dispatcher(request, err)
  
  return redirect(urls.reverse('workspaces'))