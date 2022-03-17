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
  
  if request.method == 'GET': return render(request, 'common_form.html', context)
  else:
    bounded_card_form = CardForm(request.POST)
    try:
      if bounded_card_form.is_valid():
        cleanded_data = bounded_card_form.cleaned_data
        title = cleanded_data['title']
        board = Board.objects.filter(id=board_id).first()
        
        if not Card.objects.filter(Q(title=title) & Q(board__workspace_id=board.workspace_id)).exists():
          Card.objects.create(
            title = title,
            target_date = cleanded_data['target_date'],
            board_id = board_id
          )
          return HttpResponse(status=204, headers={"HX-Trigger": f"cardAdded-{encrypted_board_id}"})
        
        messages.warning(request, Const.ALREADY_EXISTS_CARD)
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
    
    except Exception as err:
      exception_message_dispatcher(request, err)
    
    context['form'] = bounded_card_form
    context['partial'] = True
    
    return render(request, 'common_form.html', context)