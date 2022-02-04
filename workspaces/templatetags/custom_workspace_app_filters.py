import base64
from django import template
from helpers import Helper

register = template.Library()

@register.filter
def encrypt_id(id: int) -> str:
  plain_string = str(id) + Helper.get_encryption_key()
  my_bytes = plain_string.encode('utf-8')
  return base64.b64encode(my_bytes).decode('utf-8')
