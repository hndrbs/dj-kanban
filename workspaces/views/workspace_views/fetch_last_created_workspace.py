from .importer import *
from django.shortcuts import render as djrender

@require_http_methods(["GET"])
@login_required
def fetch_last_created_workspace(request: HttpRequest) -> HttpResponse:
  workspace = Workspace.objects.order_by('-created_at').first()
  context = {
    "workspace": workspace,
    "partial": True
  }
  
  messages.success(request, "successfully save new workspace")

  return djrender(request, "components/workspace.html", context)