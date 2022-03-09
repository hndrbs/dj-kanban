from .importer import *


@login_required
@require_http_methods(['GET', 'POST'])
def add_card(request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  context = {
    'form': CardForm(),
    'title_form': 'Add card',
    'submit_button_name': 'Add card'
  }
  board_id = get_model_id(encrypted_board_id)
  
  if request.method == 'GET':
    try:
      if Board.objects.filter(id=board_id).exists():
        return render(request, 'form_card.html', context)
    
      messages.warning(request, Const.NOT_FOUND_BOARD)

    except Exception as err:
      exception_message_dispatcher(request, err)

    return redirect(urls.reverse('workspaces'))
  
  else:
    bounded_card_form = CardForm(request.POST)
    try:
      if bounded_card_form.is_valid():
        Card.objects.create(
          title = bounded_card_form.cleaned_data['title'],
          target_date = bounded_card_form.cleaned_data['target_date'],
          board_id = board_id
        )
        board = Board.objects.get(id=board_id)
        return redirect(urls.reverse('boards', args=[encrypt_id(board.workspace_id)]))

      messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
    
    except Exception as err:
      exception_message_dispatcher(request, err)
    
    context['form'] = bounded_card_form
    
    return render(request, 'form_card.html', context)