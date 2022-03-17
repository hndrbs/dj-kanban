from .importer import *

@require_http_methods(["POST", "GET"])
@login_required
def delete_board(request: HttpRequest) -> HttpResponse:
  
  if request.method == 'GET':
    encrypted_id = request.GET.get('id')
    id = get_model_id(encrypted_id)
    dialog_confirmation = "Are you sure to delete this board? " + \
                          "you might lose all of cards you've created and there is no way to get them back!"

    context = {
      "model_id": id,
      "dialog_confirmation": dialog_confirmation,
      "model_name": "board" 
    }
    return render(request, "confirmation.html", context)

  else:
    try:
      encrypted_board_id = request.POST.get('id')
      board_id = get_model_id(encrypted_board_id)
      
      board = Board.objects.filter(Q(id=board_id))

      if board.exists():
        board.delete()
        messages.success(request, "Successfully to delete a board")
        response = djrender(request, "messages.html")
        response["HX-Trigger"] = f"boardDeleted-{encrypted_board_id}"
        return response
      
      messages.warning(request, Const.NOT_FOUND_BOARD)

    except Exception as err:
      exception_message_dispatcher(request, err)
    
    return redirect(urls.reverse('workspaces'))
    