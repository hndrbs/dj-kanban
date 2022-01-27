
from unicodedata import name
from django.urls import path
from .views import loginView, registerView, logoutView

urlpatterns = [
    path('register', registerView, name='register'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout')
]
