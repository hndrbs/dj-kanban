from django.contrib.auth.models import User as DefaultUserClass
# Create your models here.

class User(DefaultUserClass):
  class Meta:
    db_table = "Users"