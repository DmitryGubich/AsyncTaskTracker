import uuid

from django.db import models


class AuthUser(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    public_id = models.UUIDField()
    role = models.CharField(choices=ROLE_CHOICES, default="user", max_length=254)


class Task(models.Model):
    STATUS_CHOICES = (
        ("done", "Done"),
        ("in_progress", "In Progress"),
    )
    public_id = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=254)
    status = models.CharField(
        choices=STATUS_CHOICES, default="in_progress", max_length=254
    )
    assignee = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
