from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    ROLE_CHOICES = (
        ("ADMIN", "admin"),
        ("USER", "user"),
        ("MANAGER", "manager"),
    )

    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default="USER", max_length=15)
