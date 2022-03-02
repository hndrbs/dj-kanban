from .importer import *

@login_required
@require_http_methods(['POST'])
def delete_card(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  try:
    card_id = get_model_id(request.POST.get('card_id'))
    Card.objects.filter(id=card_id).delete()
    messages.success(request, 'successfully to delete card')

  except Exception as err:
    messages.error(request, str(err))
    messages.error(request, Const.EXCEPTION_MESSAGE)

  return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))