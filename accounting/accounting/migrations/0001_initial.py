# Generated by Django 4.2.4 on 2023-08-18 19:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("public_id", models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name="AuthUser",
            fields=[
                ("public_id", models.UUIDField(primary_key=True, serialize=False)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("manager", "Manager"),
                            ("user", "User"),
                        ],
                        default="user",
                        max_length=254,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("public_id", models.UUIDField(primary_key=True, serialize=False)),
                ("description", models.CharField(max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[("done", "Done"), ("in_progress", "In Progress")],
                        max_length=254,
                    ),
                ),
                ("assigned_date", models.DateField(auto_now_add=True)),
                ("price", models.IntegerField(default=0)),
                ("fee", models.IntegerField(default=0)),
                (
                    "assignee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounting.authuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Balance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("debit", models.IntegerField(default=0)),
                ("credit", models.IntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounting.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(max_length=1024)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounting.authuser",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounting.authuser"
            ),
        ),
    ]
