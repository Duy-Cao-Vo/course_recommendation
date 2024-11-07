# # some_app/models.py
from django.db import models
from usermanagement.models import MyUser

class SomeModel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)