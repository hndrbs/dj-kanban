from .importer import *

@require_http_methods(["POST", "GET"])
@login_required(login_url=login_url)
def delete_workspace(request: HttpRequest) -> HttpResponse:
  if request.method == "POST":
    try:
      encrypted_id = request.POST.get('id')
      id = get_model_id(encrypted_id)
      Workspace.objects.filter(id=id).delete()
      messages.success(request, "successfully delete a workspace")
      return djrender(request, "messages.html")
      
    except Workspace.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_WORKSPACE)

    except Exception as err:
      exception_message_dispatcher(request, err)
    
    return redirect(urls.reverse('workspaces'))
  
  else:
    encrypted_id = request.GET.get('id')
    id = get_model_id(encrypted_id)
    dialog_confirmation = "Are you sure to delete this workspace? " + \
                          "you might lose all the boards and cards you've created and there is no way to get them back!"

    context = {
      "model_id": id,
      "dialog_confirmation": dialog_confirmation,
      "model_name": "workspace" 
    }
    return render(request, "confirmation.html", context)