from django.db import models
# Create your models here.


class Workspace(models.Model):
  class Meta:
    db_table = 'Workspaces'
    ordering = ['-id', '-is_active', '-updated_at', '-created_at']
  
  id = models.BigIntegerField(primary_key=True)
  desc = models.TextField(max_length=1000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
  is_active = models.BooleanField()