import json
import logging

import pika

logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost", heartbeat=600, blocked_connection_timeout=300
    )
)
channel = connection.channel()


def publish(event, body):
    dump_body = json.dumps(body)
    logger.info(f"UserStreaming event: '{event}' with body: {dump_body}")

    properties = pika.BasicProperties(event)
    channel.basic_publish(
        exchange="",
        routing_key="UserStreaming",
        body=dump_body,
        properties=properties,
    )
