# Generated by Django 4.2.4 on 2023-08-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0002_remove_authuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="fee",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="task",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]
