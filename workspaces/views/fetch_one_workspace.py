from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_one_workspace(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  id = get_model_id(encrypted_workspace_id)
  workspace = Workspace.objects.filter(id=id).first()
  context = {
    "workspace": workspace,
    "partial": True
  }
  
  messages.success(request, "successfully edit a workspace")

  return djrender(request, "components/workspace.html", context)