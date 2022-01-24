
from django.urls import path
from .views import loginView, registerView

urlpatterns = [
    path('register', registerView, name='register'),
    path('login', loginView, name='login')
]
