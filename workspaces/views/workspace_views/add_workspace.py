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
    return render(request, 'common_form.html', context)

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

          return HttpResponse(status=204, headers={"HX-Trigger": "movieAdded"})
        
        else:
          messages.warning(request, "Looks like workspace with this title already exists")
      
      else:      
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)

      
    except Exception as err:
      exception_message_dispatcher(request, err)
      
    context['form'] = form
    context['partial'] = True
    
    return render(request, 'common_form.html', context=context)