# django's modules
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django import urls
from helpers import (
  custom_render as render,
  get_model_id,
  exception_message_dispatcher
)
# my modules
from constants import Constant as Const
from workspaces.forms import WorkspaceForm
from workspaces.models import Workspace, WorkspaceMember

login_url = "/auth/login"
