from .importer import *

@login_required
@require_http_methods(['POST', 'GET'])
def delete_card(request: HttpRequest) -> HttpResponse:
  if request.method == "GET":
    encrypted_id = request.GET.get('id')
    id = get_model_id(encrypted_id)
    dialog_confirmation = "Are you sure to delete this card?"

    context = {
      "model_id": id,
      "dialog_confirmation": dialog_confirmation,
      "model_name": "card" 
    }
    return render(request, "confirmation.html", context)

  else:
    try:
      card_id = get_model_id(request.POST.get('id'))
      Card.objects.filter(id=card_id).delete()
      messages.success(request, 'successfully to delete a card')
      return djrender(request, "messages.html")

    except Exception as err:
      exception_message_dispatcher(request, err)

    return redirect(urls.reverse('workspaces'))