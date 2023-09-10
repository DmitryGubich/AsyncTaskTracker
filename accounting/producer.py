import datetime
import json
import logging
import uuid

import pika
from async_task_tracker_schemas.schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters("broker", heartbeat=600, blocked_connection_timeout=300)
)
channel = connection.channel()

channel.exchange_declare(exchange="AccountBusinessEvents", exchange_type="fanout")


def publish(event):
    event_body = {
        "event_id": str(uuid.uuid4()),
        "event_version": event["version"],
        "event_name": event["event"],
        "event_time": str(datetime.datetime.now()),
        "producer": "AsyncTaskTracker.Accounting",
        "data": event["body"],
    }
    SchemaRegistry.validate_event(
        event=event["event"], body=event_body, version=event["version"]
    )
    logger.info(f"AccountBusinessEvents event: {json.dumps(event_body)}")

    properties = pika.BasicProperties(event["event"])
    channel.basic_publish(
        exchange="AccountBusinessEvents",
        routing_key="",
        body=json.dumps(event_body),
        properties=properties,
    )
