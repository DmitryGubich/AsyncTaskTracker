import json
import logging

import pika
from async_task_tracker_schemas.events import Accounting
from async_task_tracker_schemas.schema_registry import SchemaRegistry
from django.core.management.base import BaseCommand

from analytics.models import Balance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="broker"))
        channel = connection.channel()

        channel.exchange_declare(
            exchange="AccountBusinessEvents", exchange_type="fanout"
        )
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="AccountBusinessEvents", queue=queue_name)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            SchemaRegistry.validate_event(
                event=data["event_name"],
                body=data,
                version=data["event_version"],
            )
            logger.info(
                f"Event: '{properties.content_type}' v{data['event_version']} with body: {data}"
            )
            body = data.get("data")
            if properties.content_type == Accounting.BALANCE_CREATED:
                Balance.objects.create(
                    account=body["account"],
                    debit=int(body["debit"]),
                    credit=int(body["credit"]),
                )

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
