import inspect
import uuid

from async_task_tracker_schemas.events import Auth
from django.contrib.auth.models import AbstractUser
from django.db import models
from producer import publish


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("user", "User"),
    )
    public_id = models.UUIDField(default=uuid.uuid4)
    role = models.CharField(choices=ROLE_CHOICES, default="user", max_length=254)

    def save(self, *args, **kwargs):
        create = not self.pk
        super().save(*args, **kwargs)
        if create:
            # create
            publish(
                event={
                    "event": Auth.USER_CREATED,
                    "body": {
                        "public_id": str(self.public_id),
                        "role": self.role,
                    },
                    "version": 1,
                }
            )
        else:
            # update
            publish(
                event={
                    "event": Auth.USER_UPDATED,
                    "body": {
                        "public_id": str(self.public_id),
                        "role": self.role,
                    },
                    "version": 1,
                }
            )

    def delete(self, using=None, keep_parents=False):
        super().delete(using=None, keep_parents=False)
        publish(
            event={
                "event": Auth.USER_DELETED,
                "body": {
                    "public_id": str(self.public_id),
                },
                "version": 1,
            }
        )

    def __str__(self):
        return str(self.public_id)
