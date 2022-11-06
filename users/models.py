from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField()
    is_owner = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    message = models.CharField(null=True, blank=True, max_length=127)
    is_superuser = models.BooleanField(null=True, blank=True, default=False)

    REQUIRED_FIELDS = ['password',
                       'first_name', 'last_name', 'birthdate', 'is_owner']
