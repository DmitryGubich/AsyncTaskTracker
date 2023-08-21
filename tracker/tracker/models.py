import random
import uuid

from django.core.exceptions import ValidationError
from django.db import models


class AuthUser(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    public_id = models.UUIDField(primary_key=True)
    role = models.CharField(choices=ROLE_CHOICES, default="user", max_length=254)

    def __str__(self):
        return str(self.public_id)


class Task(models.Model):
    STATUS_CHOICES = (
        ("done", "Done"),
        ("in_progress", "In Progress"),
    )
    public_id = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=254)
    jira_id = models.CharField(max_length=254)
    status = models.CharField(
        choices=STATUS_CHOICES, default="in_progress", max_length=254
    )
    assignee = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    price = models.IntegerField(default=0)
    fee = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price = random.randint(10, 20)
        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if "[" or "]" in self.description:
            raise ValidationError("You can not put jira id on title field")

    def __str__(self):
        return str(self.public_id)
