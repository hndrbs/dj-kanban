# django's modules
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django import urls
from helpers import Helper, customer_render as render
# my modules
from workspaces.contants import Constant as Const
from workspaces.forms import WorkspaceForm
from workspaces.models import Workspace, WorkspaceMember

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
        title = form.cleaned_data['title']
        user = request.user
        
        if not Workspace.objects.filter(Q(title=title) & Q(owner=user)).exists():

          new_workspace = Workspace.objects.create(
            title=title,
            desc=form.cleaned_data['desc'],
            owner=request.user
          )
          WorkspaceMember.objects.create(
            member=request.user,
            workspace=new_workspace
          )
          messages.success(request, "successfully save new workspace")
          return redirect(urls.reverse(Const.WORKSPACES_URL))
        
        else:
          messages.warning(request, "Looks like workspace with this title already exists")
      
      else:      
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
      
    except Exception as err:
      messages.error(request, str(err))
      # messages.error(request, "something went wrong, you may try again or if error persists, cantact us")
      messages.error(request, Const.EXCEPTION_MESSAGE)
      
    context['form'] = form
    return render(request, 'form_workspace.html', context)

@require_http_methods(["GET", "POST"])
@login_required(login_url=login_url)
def edit_workspace(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  context = {
    'submit_button_name': 'Edit Workspace',
    'title_form': 'Edit Workspace'
  }
  
  if request.method == "GET":
    try:
      id = Helper.get_model_id(encrypted_workspace_id)
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
      id = Helper.get_model_id(encrypted_workspace_id)
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

@require_http_methods(["POST"])
@login_required(login_url=login_url)
def deactivate_workspace(request: HttpRequest) -> HttpResponse:
  try:
    encrypted_id = request.POST.get('id')
    id = Helper.get_model_id(encrypted_id)
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

