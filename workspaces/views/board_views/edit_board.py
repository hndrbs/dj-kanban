from .importer import *

@login_required
@require_http_methods(['GET', 'POST'])
def edit_board_title(request: HttpRequest, encrypted_workspace_id: str, encrypted_board_id: str) -> HttpResponse:
  context = {
    'title_form': 'Edit Board',
    'submit_button_name': 'Edit Board',
    'cancel_url': urls.reverse('boards', args=[encrypted_workspace_id])
  }

  board_id = get_model_id(encrypted_board_id)
  
  if request.method == 'GET':
    try:
      board = Board.objects.get(id=board_id)
      context['form'] = BoardForm(instance=board)
      
      return render(request, 'common_form.html', context)
    
    except Board.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_BOARD)
    
    except Exception as err:
      exception_message_dispatcher(request, err)
    
    return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))

  else:
    form = BoardForm(request.POST)
    try:
      if form.is_valid():
        workspace_id = get_model_id(encrypted_workspace_id)
        title = form.cleaned_data['title']
        
        if not Board.objects\
            .filter(
              Q(title=title) 
              & Q(workspace_id=workspace_id) 
              & ~Q(id=board_id)
            ).exists():
          board = Board.objects.get(id=board_id)
          board.title = title
          board.save()
          return HttpResponse(status=204, headers={"HX-Trigger": f"boardEdited-{encrypted_board_id}"})
        
        else:
          messages.warning(request, Const.ALREADY_EXISTS_BOARD)
      
      else:  
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except (Workspace.DoesNotExist):
      messages.warning(request, Const.NOT_FOUND_WORKSPACE)
    
    except Exception as err:
      exception_message_dispatcher(request, err)
    
    context['form'] = form
    context['partial'] = True
    return render(request, 'common_form.html', context)