from django import template
from helpers import encrypt_id

register = template.Library()

register.filter('encrypt_id', encrypt_id)

