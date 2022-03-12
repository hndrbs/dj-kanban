from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django import urls
# my modules
from constants import Constant as Const
from workspaces.forms import BoardForm
from workspaces.models import Board, Card, Workspace

from helpers import (
  get_model_id, 
  custom_render as render,
  exception_message_dispatcher
)
