import json
import logging

import pika
from django.core.management.base import BaseCommand
from uber_popug_schemas.events import Auth
from uber_popug_schemas.schema_registry import SchemaRegistry

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
            SchemaRegistry.validate_event(**data)
            logger.info(f"Event: '{properties.content_type}' with body: {data}")
            body = data.get("body")
            if properties.content_type == Auth.USER_CREATED:
                user = AuthUser.objects.create(
                    public_id=body["public_id"],
                    role=body["role"],
                )
                user.save()
            elif properties.content_type == Auth.USER_UPDATED:
                user = AuthUser.objects.get(public_id=body["public_id"])
                user.role = body["role"]
                user.save()
            elif properties.content_type == Auth.USER_DELETED:
                user = AuthUser.objects.get(public_id=body["public_id"])
                user.delete()

            logger.info("-" * 100)

        channel.basic_consume(
            queue="UserStreaming", on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
