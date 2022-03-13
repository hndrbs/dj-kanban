from .importer import *

@require_http_methods(["GET"])
@login_required
def fetch_all_workspaces(request: HttpRequest) -> HttpResponse:
  user = request.user
  workspaces = Workspace.objects.filter(Q(owner_id=user.id) & Q(is_active=True))
  # this query needs to be optimized by using pagination
  context = {
    'workspaces': workspaces
  }
  
  return render(request, 'workspaces.html', context)