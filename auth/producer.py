import json
import logging

import pika
from uber_popug_schemas.schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost", heartbeat=600, blocked_connection_timeout=300
    )
)
channel = connection.channel()


def publish(event):
    SchemaRegistry.validate_event(**event)

    body = event["body"]
    event_type = event["event"]
    version = event["version"]
    logger.info(f"UserStreaming event: '{event_type} v{version}' with body: {body}")

    properties = pika.BasicProperties(event_type)
    channel.basic_publish(
        exchange="",
        routing_key="UserStreaming",
        body=json.dumps(body),
        properties=properties,
    )
