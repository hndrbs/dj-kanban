from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.core import exceptions
from django.db.models import Q
from django import urls
from .models import User
from helpers import customer_render as render

should_unauthenticated = user_passes_test(lambda user : not user.is_authenticated, "/", redirect_field_name=None)

@should_unauthenticated
@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
  if request.method == "GET":
    context = {
      'form': RegisterForm()
    }
    return render(request, "register.html", context)
  
  else:
    form = RegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "success to register")
      return redirect(urls.reverse('login'))
    
    return render(request, "register.html", { "form": form })

@should_unauthenticated
@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
  if request.method == "GET":
    context = {
      'form': LoginForm()
    }  
    return render(request, "login.html", context)
  
  else:
    form = LoginForm(request.POST)
    context = {
      'form': form
    }
    try:
      if form.is_valid():
        username_or_email = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']
        
        user: User = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
        
        if user is not None and user.check_password(password):
          messages.success(request, "success to login")
          login(request, user)
          return redirect(urls.reverse('workspaces'))

        messages.warning(request, "username or email cannot be found")
        
    except exceptions.ObjectDoesNotExist:
      messages.warning(request, "username or email cannot be found")
    
    except Exception as err:
      messages.error(request, "something went wrong, it's on us, we are sorry")
    
    return render(request, "login.html", context)

@require_http_methods(["GET"])
def logout_view(request: HttpRequest) -> HttpResponse:
  logout(request)

  return redirect(urls.reverse("login"))