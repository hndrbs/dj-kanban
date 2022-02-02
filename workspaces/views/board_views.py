from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django import urls
# my modules
from workspaces.contants import Constant as Const
from workspaces.models import Board, Workspace

@login_required
@require_http_methods(["GET"])
def fetch_all_boards(request: HttpRequest, base64_workspace_id: str) -> HttpResponse:
  try:
    workspace_id = Workspace.get_workspace_id(base64_workspace_id)
    workspace = Workspace.objects.get(id=workspace_id)
    boards = Board.objects.filter(workspace_id=workspace_id)
    context = {
      'boards': boards,
      'workspace_title': workspace.title
    }
    
    return render(request, 'boards.html', context)
  
  except Workspace.DoesNotExist:
    messages.warning(request, Const.NOT_FOUND_MESSAGE)
  
  except Exception as err:
    messages.error(request, str(err))
    messages.error(request, Const.EXCEPTION_MESSAGE)
  
  return redirect(urls.reverse(Const.WORKSPACES_URL))