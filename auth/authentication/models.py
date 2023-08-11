from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "admin"),
        ("USER", "user"),
        ("MANAGER", "manager"),
    )

    role = models.CharField(choices=ROLE_CHOICES, default="USER", max_length=15)
