import uuid

from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    public_id = models.UUIDField(primary_key=True)
    role = models.CharField(choices=ROLE_CHOICES, default="user", max_length=254)


class Task(models.Model):
    STATUS_CHOICES = (
        ("done", "Done"),
        ("in_progress", "In Progress"),
    )
    public_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=254)
    status = models.CharField(
        choices=STATUS_CHOICES, default="in_progress", max_length=254
    )
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
