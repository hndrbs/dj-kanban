from django import urls
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from workspaces.forms import WorkspaceForm
from .models import Workspace
from django.contrib import messages

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

@require_http_methods(["GET", "POST"])
@login_required(login_url=login_url)
def add_workspace(request: HttpRequest):
  if request.method == "GET":
    context = {
      'form': WorkspaceForm()
    }
    return render(request, 'add_workspace.html', context)

  else:
    form = WorkspaceForm(request.POST)
    try:
      if form.is_valid():
        new_workspace = Workspace(
          title=form.cleaned_data['title'],
          desc=form.cleaned_data['desc'],
          owner=request.user
        )
        new_workspace.save()

        messages.success(request, "successfully save new workspace")
        return redirect(urls.reverse("workspaces"))
      
      messages.warning(request, "something wrong in the data you submitted, could you please re-check it ?")
      
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, "something went wrong, you may try again or if error persists, cantact us")
    
    return render(request, 'add_workspace.html', { 'form':  form })
      