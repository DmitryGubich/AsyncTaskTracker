import json
import logging

import pika
from async_task_tracker_schemas.schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters("broker", heartbeat=600, blocked_connection_timeout=300)
)
channel = connection.channel()

channel.exchange_declare(exchange="BalanceStreaming", exchange_type="fanout")


def publish(event):
    SchemaRegistry.validate_event(**event)
    logger.info(
        f"BalanceStreaming event: '{event['event']} v{event['version']}' with body: {event['body']}"
    )

    properties = pika.BasicProperties(event["event"])
    channel.basic_publish(
        exchange="BalanceStreaming",
        routing_key="",
        body=json.dumps(event),
        properties=properties,
    )