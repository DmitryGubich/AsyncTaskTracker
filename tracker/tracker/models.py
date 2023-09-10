import random
import uuid

from async_task_tracker_schemas.events import Tracker
from django.core.exceptions import ValidationError
from django.db import models
from producer import publish


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
        create = not self.pk
        super().save(*args, **kwargs)

        if create:
            # create
            publish(
                event={
                    "event": Tracker.TASK_ASSIGNED,
                    "body": {
                        "public_id": str(self.public_id),
                        "description": self.description,
                        "jira_id": self.jira_id,
                        "status": self.status,
                        "assignee": str(self.assignee),
                        "price": self.price,
                        "fee": self.fee,
                    },
                    "version": 3,
                }
            )
        else:
            # update
            publish(
                event={
                    "event": Tracker.TASK_COMPLETED,
                    "body": {
                        "public_id": str(self.public_id),
                        "description": self.description,
                        "jira_id": self.jira_id,
                        "status": self.status,
                        "assignee": str(self.assignee),
                        "fee": self.fee,
                        "price": self.price,
                    },
                    "version": 3,
                }
            )

    def clean(self, *args, **kwargs):
        if "[" or "]" in self.description:
            raise ValidationError("You can not put jira id on title field")

    def __str__(self):
        return str(self.public_id)
