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
        Card.objects.create(
          title = bounded_card_form.cleaned_data['title'],
          target_date = bounded_card_form.cleaned_data['target_date'],
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
  
  else:
    try:
      bounded_card_form = CardForm(request.POST)
      if bounded_card_form.is_valid():
        new_title = bounded_card_form.cleaned_data['title']
        workspace_id = Helper.get_model_id(encrypted_workspace_id)
        cards = Card.objects.filter(Q(id=card_id) & Q(board_id=board_id) & Q(board__workspace_id=workspace_id))
        if cards.exists():
          if not Card.objects.filter(Q(title=new_title) & Q(board__workspace_id=workspace_id)).exists():
            card = cards.first()
            card.title = bounded_card_form.cleaned_data['title']
            card.target_date = bounded_card_form.cleaned_data['target_date']
            card.save()
            return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))
          else:
            messages.warning(request, Const.ALREADY_EXISTS_CARD)
        else:
          messages.warning(request, Const.NOT_FOUND_CARD)      
      else:
        messages.warning(request, Const.BAD_SUBMITTED_DATA_MESSAGE)

    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    return redirect(urls.reverse('edit-card', args=[encrypted_workspace_id, encrypted_board_id, encrypted_card_id]))


@login_required
@require_http_methods(['POST'])
def delete_card(request: HttpRequest, encrypted_workspace_id: str) -> HttpResponse:
  try:
    card_id = Helper.get_model_id(request.POST.get('card_id'))
    Card.objects.filter(id=card_id).delete()
    messages.success(request, 'successfully to delete card')

  except Exception as err:
    messages.error(request, str(err))
    messages.error(request, Const.EXCEPTION_MESSAGE)

  return redirect(urls.reverse('boards', args=[encrypted_workspace_id]))


@login_required
@require_http_methods(['POST'])
def move_card_to_another_board(request: HttpRequest) -> HttpResponse:
  data = request.POST
  board_id_from = Helper.get_model_id(data.get('board_from'))
  board_id_to = Helper.get_model_id(data.get('board_to'))
  card_id = Helper.get_model_id(data.get('card_id'))
  workspace_id = Helper.get_model_id(data.get('workspace_id'))

  current_card = Card.objects.filter(Q(id=card_id) & Q(board_id=board_id_from))
  is_card_exist_in_this_board = current_card.exists()
  is_next_board_exist = Board.objects.filter(Q(id=board_id_to) & Q(workspace_id=workspace_id))
  
  if is_card_exist_in_this_board and is_next_board_exist:
    card = current_card.first()
    card.board_id = board_id_to
    card.save()
    return redirect(urls.reverse('boards', args=[data.get('workspace_id')]))
  else:
    messages.warning(request, Const.INVALID_MOVE_CARD)
    return redirect(urls.reverse('boards', args=[data.get('workspace_id')]))
  
