import json
import logging

import pika
from async_task_tracker_schemas.events import Auth
from async_task_tracker_schemas.schema_registry import SchemaRegistry
from django.core.management.base import BaseCommand

from analytics.models import AuthUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="broker"))
        channel = connection.channel()

        channel.exchange_declare(exchange="UserStreaming", exchange_type="fanout")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="UserStreaming", queue=queue_name)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            SchemaRegistry.validate_event(**data)
            logger.info(
                f"Event: '{properties.content_type}' v{data['version']} with body: {data['body']}"
            )
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

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
