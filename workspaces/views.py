from django import urls
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from .models import Workspace

login_url = "/auth/login"

@require_http_methods(["GET"])
@login_required(login_url=login_url)
def fetch_all_workspaces(request: HttpRequest) -> HttpResponse:
  user = request.user
  workspaces = Workspace.objects.filter(owner_id=user.id)
  context = {
    'workspaces': workspaces
  }
  
  return render(request, 'workspaces.html', context)

