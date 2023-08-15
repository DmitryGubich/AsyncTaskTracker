import json
import logging

import pika
from django.core.management.base import BaseCommand

from tracker.models import AuthUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.queue_declare(queue="UserStreaming", durable=True)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"Event: '{properties.content_type}' with body: {data}")

            if properties.content_type == "User.Created":
                user = AuthUser.objects.create(
                    public_id=data["public_id"],
                    role=data["role"],
                )
                user.save()
            elif properties.content_type == "User.Updated":
                user = AuthUser.objects.get(public_id=data["public_id"])
                user.role = data["role"]
                user.save()
            elif properties.content_type == "User.Deleted":
                user = AuthUser.objects.get(public_id=data["public_id"])
                user.delete()

            logger.info("-" * 50)

        channel.basic_consume(
            queue="UserStreaming", on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
