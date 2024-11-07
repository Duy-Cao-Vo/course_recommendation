from ctypes import Structure
from django.db import models
from django.contrib.auth.models import AbstractUser
from neomodel import StructuredNode, StringProperty, IntegerProperty, DateProperty, RelationshipTo, RelationshipFrom,FloatProperty
from django_neomodel import DjangoNode
from django.utils.translation import gettext_lazy as _
import webcourse.models
# Create your models here.
class MyUser(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True, error_messages={
            'unique': _("A user with that email already exists."),
        })
    isBasicUser = models.BooleanField(default=False)
    isDataAdmin = models.BooleanField(default=False)
    isAccountAdmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
