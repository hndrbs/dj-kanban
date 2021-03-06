from .importer import *


@login_required
@require_http_methods(['GET', 'POST'])
def edit_card(request: HttpRequest, encrypted_board_id:str,  encrypted_card_id: str) -> HttpResponse:
  context = {
    'title_form': f'Edit card',
    'submit_button_name': f"Edit card"
  }
  card_id = get_model_id(encrypted_card_id)
  board_id = get_model_id(encrypted_board_id)
  card = Card.objects.filter(Q(id=card_id) & Q(board_id=board_id))

  if request.method == 'GET':
    context['form'] = CardForm(instance=card.first())
    return render(request, 'common_form.html', context)

  else:
    try:
      bounded_card_form = CardForm(request.POST)
      if bounded_card_form.is_valid():
        new_title = bounded_card_form.cleaned_data['title']
        board = Board.objects.filter(id=board_id).first()
        workspace_id = board.workspace_id

        if not Card.objects.filter(
                Q(title=new_title) & Q(board__workspace_id=workspace_id) & ~Q(id=card_id)).exists():

          card = Card.objects.filter(Q(id=card_id) & Q(board_id=board_id) & Q(board__workspace_id=workspace_id)).first()
          card.title = bounded_card_form.cleaned_data['title']
          card.target_date = bounded_card_form.cleaned_data['target_date']
          card.save()
          
          return HttpResponse(status=204, headers={"HX-Trigger": f"cardEdited-{encrypted_card_id}"})

        
        messages.warning(request, Const.ALREADY_EXISTS_CARD)
      
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)

    except Exception as err:
      exception_message_dispatcher(request, err)

    context['form'] = bounded_card_form
    context['partial'] = True

    return render(request, 'common_form.html', context)