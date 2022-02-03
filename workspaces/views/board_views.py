from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django import urls
# my modules
from workspaces.contants import Constant as Const
from workspaces.forms import BoardForm
from workspaces.models import Board, Workspace

@login_required
@require_http_methods(["GET"])
def fetch_all_boards(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  try:
    workspace_id = Workspace.get_workspace_id(encrypted_workspace_id)
    workspace = Workspace.objects.get(id=workspace_id)
    boards = Board.objects.filter(workspace_id=workspace_id)
    context = {
      'boards': boards,
      'workspace': workspace
    }
    
    return render(request, 'boards.html', context)
  
  except Workspace.DoesNotExist:
    messages.warning(request, Const.NOT_FOUND_MESSAGE)
  
  except Exception as err:
    print(err)
    messages.error(request, str(err))
    messages.error(request, Const.EXCEPTION_MESSAGE)
  
  return redirect(urls.reverse(Const.WORKSPACES_URL))

@login_required
@require_http_methods(["GET", "POST"])
def add_board(request: HttpRequest, encrypted_workspace_id: str, workspace_title: str)-> HttpResponse:
  context = {
    'form': BoardForm(),
    'title_form': f'Add board on {workspace_title}',
    'submit_button_name': f"Add Board"
  }
  
  if request.method == 'GET':
    return render(request, 'form_board.html', context)

  else:
    form = BoardForm(request.POST)
    try:
      if form.is_valid():
        workspace = Workspace.objects.get(id=Workspace.get_workspace_id(encrypted_workspace_id))
        existing_boards = Board.objects.filter(workspace=workspace)
        Board.objects.create(
          title=form.cleaned_data['title'],
          workspace=workspace,
          board_number=existing_boards.count() + 1
        )
        
        messages.success(request, f'successfully add board on {workspace_title}')
        return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))
      
      messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except (Workspace.DoesNotExist, Board.DoesNotExist):
      messages.warning(request, Const.NOT_FOUND_MESSAGE)
    
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    context['form'] = form
    return render(request, 'form_board.html', context)
    