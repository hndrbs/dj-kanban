import base64
from django import urls
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from workspaces.forms import WorkspaceForm
from .models import Workspace
from django.contrib import messages
from django.db.models import Q

login_url = "/auth/login"

@require_http_methods(["GET"])
@login_required(login_url=login_url)
def fetch_all_workspaces(request: HttpRequest) -> HttpResponse:
  user = request.user
  workspaces = Workspace.objects.filter(Q(owner_id=user.id) & Q(is_active=True))
  context = {
    'workspaces': workspaces
  }
  
  return render(request, 'workspaces.html', context)

@require_http_methods(["GET", "POST"])
@login_required(login_url=login_url)
def add_workspace(request: HttpRequest):
  context = {
    'form': WorkspaceForm(),
    'submit_button_name': 'Add Workspace',
    'title_form': 'Add Workspace'
  }
  
  if request.method == "GET":
    return render(request, 'form_workspace.html', context)

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
      
    context['form'] = form
    return render(request, 'form_workspace.html', context)

@require_http_methods(["GET", "POST"])
@login_required(login_url=login_url)
def edit_workspace(request: HttpRequest, b64_id: str) -> HttpResponse:
  context = {
    'submit_button_name': 'Edit Workspace',
    'title_form': 'Edit Workspace'
  }
  
  if request.method == "GET":
    try:
      id = Workspace.get_workspace_id(b64_id)
      workspace = Workspace.objects.get(id=id)
      form = WorkspaceForm(instance=workspace)
      context.update({ 'form': form })
      return render(request, 'form_workspace.html', context)
    
    except Workspace.DoesNotExist:
      messages.warning(request, "we cannot find your workspace, may be you've deleted it ?. please reload the page")
    
    except Exception as err:
      messages.error(str(err))
      messages.error(request, "something went wrong, you may try again or if error persists, cantact us")
      return redirect(urls.reverse('workspaces'))

@require_http_methods(["GET"])
@login_required(login_url=login_url)
def deactivate_workspace(request: HttpRequest, b64_id: str) -> HttpResponse:
  try:
    id = Workspace.get_workspace_id(b64_id)
    workspace = Workspace.objects.get(id=id)
    workspace.is_active = False
    workspace.save()
    messages.success(request, "successfully archive your workspace")
    
  except Workspace.DoesNotExist:
    messages.warning(request, "we cannot find your workspace, may be you've deleted it ?. please reload the page")

  except Exception as err:
    messages.error(str(err))
    messages.error(request, "something went wrong, you may try again or if error persists, cantact us")
  
  return redirect(urls.reverse("workspaces"))

      