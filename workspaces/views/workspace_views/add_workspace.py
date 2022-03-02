from .importer import *

@require_http_methods(["GET", "POST"])
@login_required()
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