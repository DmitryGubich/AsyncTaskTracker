import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    public_id = models.UUIDField(default=uuid.uuid4)
    role = models.CharField(choices=ROLE_CHOICES, default="user", max_length=254)
