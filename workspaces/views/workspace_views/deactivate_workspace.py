from .importer import *

@require_http_methods(["POST"])
@login_required(login_url=login_url)
def deactivate_workspace(request: HttpRequest) -> HttpResponse:
  try:
    encrypted_id = request.POST.get('id')
    id = get_model_id(encrypted_id)
    workspace = Workspace.objects.get(id=id)
    workspace.is_active = False
    workspace.save()
    messages.success(request, "successfully archive your workspace")
    
  except Workspace.DoesNotExist:
    messages.warning(request, Const.NOT_FOUND_WORKSPACE)

  except Exception as err:
    exception_message_dispatcher(request, err)
  
  return redirect(urls.reverse('workspaces'))