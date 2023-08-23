import json
import logging

import pika
from django.core.management.base import BaseCommand
from uber_popug_schemas.events import Accounting
from uber_popug_schemas.schema_registry import SchemaRegistry

from analytics.models import Balance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.exchange_declare(exchange="BalanceStreaming", exchange_type="fanout")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="BalanceStreaming", queue=queue_name)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            SchemaRegistry.validate_event(**data)
            logger.info(f"Event: '{properties.content_type}' with body: {data}")
            body = data.get("body")
            if properties.content_type == Accounting.BALANCE_CREATED:
                Balance.objects.create(
                    account=body["account"],
                    debit=int(body["debit"]),
                    credit=int(body["credit"]),
                )

            logger.info("-" * 100)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
