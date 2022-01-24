from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
# Create your views here.


@require_http_methods(["GET", "POST"])
def registerView(request: HttpRequest) -> HttpResponse:
  if request.method == "GET":
    context = {
      'form': RegisterForm()
    }
    return render(request, "register.html", context)
  
  else:
    return render(request, "register.html", { "is_post": True })
  