from helpers import Helper
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django import urls
# my modules
from workspaces.contants import Constant as Const
from workspaces.forms import  BoardForm, CardForm
from workspaces.models import Board, Card, Workspace


@login_required
@require_http_methods(['GET', 'POST'])
def add_card(request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  context = {
    'form': CardForm(),
    'title_form': f'Add card',
    'submit_button_name': f"Add card"
  }
  board_id = Helper.get_model_id(encrypted_board_id)
  
  if request.method == 'GET':
    try:
      if Board.objects.filter(id=board_id).exists():
        # context['form'] = BoardForm(instance=boards.first())
        return render(request, 'form_card.html', context)
    
      messages.warning(request, Const.NOT_FOUND_BOARD)
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    
    return redirect(urls.reverse('workspaces'))
  
  else:
    bounded_card_form = CardForm(request.POST)
    try:
      if bounded_card_form.is_valid():
        num_of_card = Card.objects.filter(board_id=board_id).count()
        Card.objects.create(
          title = bounded_card_form.cleaned_data['title'],
          target_date = bounded_card_form.cleaned_data['target_date'],
          card_number = num_of_card + 1,
          board_id = board_id
        )
        board = Board.objects.get(id=board_id)
        return redirect(urls.reverse('boards', args=[Helper.encrypt_id(board.workspace_id)]))

      messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)
    
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    context['form'] = bounded_card_form
    
    return render(request, 'form_card.html', context)



# @login_required
# @require_http_methods(['GET', 'POST'])
