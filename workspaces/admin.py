from django.contrib import admin
from .models import Workspace, Board, Card, Assignment
# Register your models here.

admin.site.register(Workspace)
admin.site.register(Board)
admin.site.register(Card)
admin.site.register(Assignment)