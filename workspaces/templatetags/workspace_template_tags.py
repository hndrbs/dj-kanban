from django import template
from helpers import Helper

register = template.Library()

register.filter('encrypt_id', Helper.encrypt_id)

