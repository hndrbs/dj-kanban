from .importer import *

@require_http_methods(["GET", "POST"])
@login_required(login_url=login_url)
def edit_workspace(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  context = {
    'submit_button_name': 'Edit Workspace',
    'title_form': 'Edit Workspace'
  }
  
  if request.method == "GET":
    try:
      id = get_model_id(encrypted_workspace_id)
      workspace = Workspace.objects.get(id=id)
      form = WorkspaceForm(instance=workspace)
      context.update({ 'form': form })
      return render(request, 'form_workspace.html', context)
    
    except Workspace.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_WORKSPACE)
    
    except Exception as err:
      exception_message_dispatcher(request, err)

    return redirect(urls.reverse('workspaces'))
  
  else:
    try:
      id = get_model_id(encrypted_workspace_id)
      workspace = Workspace.objects.get(id=id)
      form = WorkspaceForm(request.POST)
      if form.is_valid():
        
        title = form.cleaned_data['title']
        user = request.user
        
        if not Workspace.objects.filter(Q(title=title) & Q(owner=user) & ~Q(id=id)).exists():
        
          workspace.title = form.cleaned_data['title']
          workspace.desc = form.cleaned_data['desc']
          workspace.save()
          messages.success(request, "successfully edit workspace")
          
          return redirect(urls.reverse('workspaces'))

        else:
          messages.warning(request, "Looks like workspace with this title already exists")
      
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except Workspace.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_WORKSPACE)
    
    except Exception as err:
      exception_message_dispatcher(request, err)
    
    context.update({'form': form})
    
    return render(request, 'form_workspace.html', context)