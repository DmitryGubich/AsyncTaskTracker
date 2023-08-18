import random
import uuid

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
    status = models.CharField(choices=STATUS_CHOICES, max_length=254)
    assignee = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    date_created = models.DateField(auto_now_add=True)
    price = models.IntegerField()

    def save(self, *args, **kwargs):
        self.price = random.randint(10, 20)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.public_id)


class Account(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return str(self.public_id)


class AuditLog(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024)
