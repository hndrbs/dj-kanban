from .importer import *

@login_required
@require_http_methods(["GET", "POST"])
def add_board(request: HttpRequest, encrypted_workspace_id: str)-> HttpResponse:
  context = {
    'form': BoardForm(),
    'title_form': 'Add board',
    'submit_button_name': 'Add Board',
    'encrypted_workspace_id': encrypted_workspace_id
  }
  
  if request.method == 'GET':
    return render(request, 'form_board.html', context)

  else:
    form = BoardForm(request.POST)
    try:
      if form.is_valid():
        workspace_id = get_model_id(encrypted_workspace_id)
        title = form.cleaned_data['title']
        boards = Board.objects\
                  .filter(Q(title=title) & Q(workspace_id=workspace_id))

        if not boards.exists():
          workspace = Workspace.objects.get(id=get_model_id(encrypted_workspace_id))
          Board.objects.create(title=title, workspace=workspace)
          
          messages.success(request, f'successfully add board')
          return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))
        else:
          messages.warning(request, Const.ALREADY_EXISTS_BOARD)
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except Board.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_BOARD)

    except Exception as err:
      exception_message_dispatcher(request, err)
    
    context['form'] = form
    return render(request, 'form_board.html', context)