import base64
from django.db import models
# Create your models here.
from helpers import Helper

class Workspace(models.Model):
  class Meta:
    db_table = 'Workspaces'
    ordering = ['-id', '-updated_at', '-created_at']
  
  id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  desc = models.TextField(max_length=1000)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)

  def __str__(self) -> str:
      return self.title
    
  def get_base64_encoded(self):
    plain_string = str(self.id) + Helper.get_encryption_key()
    my_bytes = plain_string.encode('utf-8')
    return base64.b64encode(my_bytes).decode('utf-8')

  @staticmethod
  def get_workspace_id(b64_id: str) -> int:
    id_secret_key = base64.b64decode(b64_id).decode('utf-8')
    id = id_secret_key.split(Helper.get_encryption_key())[0]
    return int(id)
  
class Board(models.Model):
  class Meta:
    db_table = 'Boards'
    ordering = ['-id', '-updated_at', '-created_at']
  
  id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  workspace = models.ForeignKey('workspaces.Workspace', on_delete=models.CASCADE)
  board_number = models.IntegerField()

  def __str__(self) -> str:
      return self.title

class Card(models.Model):
  class Meta:
    db_table = 'Cards'
    ordering = ['-id', '-updated_at', '-created_at']
  
  id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  target_date = models.DateField()
  board = models.ForeignKey('workspaces.Board', on_delete=models.CASCADE)
  card_number = models.IntegerField()

  def __str__(self) -> str:
      return self.title
class Assignment(models.Model):
  class Meta:
    db_table = 'Assignments'
    ordering = ['-id', '-updated_at', '-created_at']
  
  id = models.BigAutoField(primary_key=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  card = models.ForeignKey('workspaces.Card', on_delete=models.CASCADE)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE)
  
  def __str__(self) -> str:
      return f'{self.card} {self.user}'

class WorkspaceMember(models.Model):
  class Meta:
    db_table = 'WorkspaceMembers'
    ordering = ['-created_at']
  
  id = models.BigAutoField(primary_key=True)
  workspace = models.ForeignKey('workspaces.Workspace', on_delete=models.CASCADE)
  member = models.ForeignKey('users.User', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)