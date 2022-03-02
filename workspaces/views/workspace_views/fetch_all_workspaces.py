from .importer import *

@require_http_methods(["GET"])
@login_required
def fetch_all_workspaces(request: HttpRequest) -> HttpResponse:
  user = request.user
  workspaces = Workspace.objects.filter(Q(owner_id=user.id) & Q(is_active=True))
  context = {
    'workspaces': workspaces
  }
  
  return render(request, 'workspaces.html', context)