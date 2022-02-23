import base64
import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

class Helper:
  @staticmethod
  def get_encryption_key():
    return os.environ.get('MODEL_ENCRYPTION_KEY')
  
  @staticmethod
  def get_model_id(encrypted_id: str) -> int:
    id_secret_key = base64.b64decode(encrypted_id).decode('utf-8')
    id = id_secret_key.split(os.environ.get('MODEL_ENCRYPTION_KEY'))[0]
    return int(id)
  
  @staticmethod
  def encrypt_id(id: int) -> str:
    plain_string = str(id) + Helper.get_encryption_key()
    my_bytes = plain_string.encode('utf-8')
    return base64.b64encode(my_bytes).decode('utf-8')
  

def customer_render(request: HttpRequest, template: str, context: dict) -> HttpResponse:
  if request.headers.get('HX-Request'):
    return render(request, template, context)
  return render(request, 'fragments/' + template, context)