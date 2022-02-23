from helpers import Helper, customer_render as render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django import urls
# my modules
from workspaces.contants import Constant as Const
from workspaces.forms import  CardForm
from workspaces.models import Board, Card


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



@login_required
@require_http_methods(['GET', 'POST'])
def edit_card(request: HttpRequest, encrypted_workspace_id:str, encrypted_board_id:str,  encrypted_card_id: str) -> HttpResponse:
  context = {
    'title_form': f'Edit card',
    'submit_button_name': f"Edit card"
  }
  card_id = Helper.get_model_id(encrypted_card_id)
  board_id = Helper.get_model_id(encrypted_board_id)
  
  if request.method == 'GET':
    try:
      card = Card.objects.filter(Q(id=card_id) & Q(board_id=board_id))
      if card.exists():
        context.update({ 'form': CardForm(instance=card.first()) })
        # context['form'] = BoardForm(instance=boards.first())
        return render(request, 'form_card.html', context)
    
      messages.warning(request, Const.NOT_FOUND_BOARD)
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    
    return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))
  
