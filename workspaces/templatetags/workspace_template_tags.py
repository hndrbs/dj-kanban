from django import template
from helpers import encrypt_id, get_next_board_id, get_previous_board_id, generate_random

register = template.Library()

register.filter('encrypt_id', encrypt_id)
register.filter('generate_random', generate_random)
register.filter('get_next_board_id', get_next_board_id)
register.filter('get_previous_board_id', get_previous_board_id)


