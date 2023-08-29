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
    public_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=254)
    jira_id = models.CharField(max_length=254, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=254)
    assignee = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    assigned_date = models.DateField(auto_now_add=True)
    price = models.IntegerField(default=0)
    fee = models.IntegerField(default=0)


class Balance(models.Model):
    account = models.UUIDField()
    debit = models.IntegerField(default=0)  # ---
    credit = models.IntegerField(default=0)  # +++
