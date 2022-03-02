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
    messages.warning(request, Const.NOT_FOUND_MESSAGE)

  except Exception as err:
    messages.error(str(err))
    messages.error(request, Const.EXCEPTION_MESSAGE)
  
  return redirect(urls.reverse(Const.WORKSPACES_URL))