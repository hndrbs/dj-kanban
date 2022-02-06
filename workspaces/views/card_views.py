from helpers import Helper
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django import urls
# my modules
from workspaces.contants import Constant as Const
from workspaces.forms import  CardForm
from workspaces.models import Board, Card, Workspace


@login_required
@require_http_methods(['GET', 'POST'])
def add_card(request: HttpRequest, encrypted_board_id: str) -> HttpResponse:
  context = {
    'form': CardForm(),
    'title_form': f'Add card',
    'submit_button_name': f"Add card"
  }
  
  if request.method == 'GET':
    try:
      board_id = Helper.get_model_id(encrypted_board_id)
      board = Board.objects.get(id=board_id)
      return render(request, 'form_card.html', context)
    except Board.DoesNotExist:
      messages.warning(request, Const.NOT_FOUND_MESSAGE)
    except Exception as err:
      messages.error(request, str(err))
      messages.error(request, Const.EXCEPTION_MESSAGE)
    
    