
from django.urls import path
from .views import registerView

urlpatterns = [
    path('register', registerView, name='register')
]
