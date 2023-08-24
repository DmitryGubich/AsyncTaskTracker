import uuid

from django.core.exceptions import ValidationError
from django.db import models
from producer import publish
from uber_popug_schemas.events import Accounting


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

    def clean(self, *args, **kwargs):
        if "[" or "]" in self.description:
            raise ValidationError("You can not put jira id on title field")

    def __str__(self):
        return str(self.public_id)


class Account(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)

    @property
    def debit(self):
        return sum(self.balance_set.values_list("debit", flat=True))

    @property
    def credit(self):
        return sum(self.balance_set.values_list("credit", flat=True))

    @property
    def balance(self):
        return self.credit - self.debit

    def __str__(self):
        return str(self.public_id)


class Balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    debit = models.IntegerField(default=0)  # ---
    credit = models.IntegerField(default=0)  # +++

    def save(self, *args, **kwargs):
        publish(
            event={
                "event": Accounting.BALANCE_CREATED,
                "body": {
                    "account": str(self.account),
                    "debit": str(self.debit),
                    "credit": str(self.credit),
                },
                "version": "1",
            }
        )
        super().save(*args, **kwargs)


class AuditLog(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024)
