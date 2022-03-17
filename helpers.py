import base64
import os
import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from constants import Constant
from workspaces.models import Board
from django.db.models import Max, Min

def get_encryption_key():
  return os.environ.get('MODEL_ENCRYPTION_KEY')
  
def get_model_id(encrypted_id: str) -> int:
  return encrypted_id
  # id_secret_key = base64.b64decode(encrypted_id).decode('utf-8')
  # id = id_secret_key.split(os.environ.get('MODEL_ENCRYPTION_KEY'))[1]
  
  # if not id.isnumeric(): return 0

  # return int(id)
  
def encrypt_id(id: int) -> str:
  return id
  # plain_string = get_encryption_key() + str(id)
  # my_bytes = plain_string.encode('utf-8')
  # return base64.b64encode(my_bytes).decode('utf-8')
  

def custom_render(request: HttpRequest, template: str, context: dict, status:int = 200) -> HttpResponse:
  if  request.headers.get('HX-Request')\
      and not request.headers.get('HX-Current-URL', '').__contains__('auth'):
    template = 'fragments/' + template
  
  return render(request, template, context=context, status=status)

def exception_message_dispatcher(request: HttpRequest, error_message: Exception):
  # this function's name should be changed
  # the name should be a "verb"
  messages.error(request, str(error_message))
  messages.error(request, Constant.EXCEPTION_MESSAGE)


def get_next_board_id(board: Board) -> int:
  return Board.objects.filter(id__gt=board.id).values_list('id').aggregate(Min('id')).get('id__min')

def get_previous_board_id(board: Board) -> int:
  return Board.objects.filter(id__lt=board.id).values_list('id').aggregate(Max('id')).get('id__max')

def generate_random(max_num: int) -> int:
  return random.randint(1, max_num)