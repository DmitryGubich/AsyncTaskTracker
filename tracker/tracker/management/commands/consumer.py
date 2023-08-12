import json

import pika
from django.core.management.base import BaseCommand

from tracker.models import AuthUser


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.queue_declare(queue="auth", durable=True)

        def callback(ch, method, properties, body):
            data = json.loads(body)

            if properties.content_type == "user_created":
                user = AuthUser.objects.create(
                    username=data["username"],
                    public_id=data["public_id"],
                    role=data["role"],
                )
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"User (public_id={user.public_id}) was created")
                )
            elif properties.content_type == "user_updated":
                user = AuthUser.objects.get(public_id=data["public_id"])
                user.role = data["role"]
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Role for user (public_id={user.public_id}) was set to {data['role']}"
                    )
                )
            elif properties.content_type == "user_deleted":
                user = AuthUser.objects.get(public_id=str(data["public_id"]))
                user.delete()
                self.stdout.write(
                    self.style.WARNING(
                        f"User (public_id={data['public_id']}) was deleted"
                    )
                )

        channel.basic_consume(queue="auth", on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
