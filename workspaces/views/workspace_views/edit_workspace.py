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
      messages.warning(request, Const.NOT_FOUND_MESSAGE)
    
    except Exception as err:
      messages.error(str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
      return redirect(urls.reverse(Const.WORKSPACES_URL))
  else:
    try:
      id = get_model_id(encrypted_workspace_id)
      workspace = Workspace.objects.get(id=id)
      form = WorkspaceForm(request.POST)
      if form.is_valid():
        
        title = form.cleaned_data['title']
        user = request.user
        
        if not Workspace.objects.filter(Q(title=title) & Q(owner=user)).exists():
        
          workspace.title = form.cleaned_data['title']
          workspace.desc = form.cleaned_data['desc']
          workspace.save()
          messages.success(request, "successfully edit workspace")
          
          return redirect(urls.reverse(Const.WORKSPACES_URL))

        else:
          messages.warning(request, "Looks like workspace with this title already exists")
      
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except Workspace.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_MESSAGE)
    
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    context.update({'form': form})
    
    return render(request, 'form_workspace.html', context)