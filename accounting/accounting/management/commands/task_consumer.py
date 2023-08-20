import json
import logging
import random

import pika
from django.core.management.base import BaseCommand
from uber_popug_schemas.events import Tracker
from uber_popug_schemas.schema_registry import SchemaRegistry

from accounting.models import Account, AuditLog, AuthUser, Balance, Task

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run consumer for rabbitmq"

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.exchange_declare(exchange="TaskStreaming", exchange_type="fanout")
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="TaskStreaming", queue=queue_name)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            SchemaRegistry.validate_event(**data)
            logger.info(f"Event: '{properties.content_type}' with body: {data}")
            body = data.get("body")
            version = data.get("version")
            if properties.content_type == Tracker.TASK_ASSIGNED:
                user = AuthUser.objects.get(public_id=body["assignee"])
                if version == "3":
                    task, _ = Task.objects.get_or_create(
                        public_id=body["public_id"],
                        defaults={
                            "description": body["description"],
                            "jira_id": body["jira_id"],
                            "status": body["status"],
                            "assignee": user,
                            "price": int(body["price"]),
                            "fee": int(body["fee"]),
                        },
                    )
                else:
                    task, _ = Task.objects.get_or_create(
                        public_id=body["public_id"],
                        defaults={
                            "description": body["description"],
                            "status": body["status"],
                            "assignee": user,
                            "price": int(body["price"]),
                            "fee": int(body["fee"]),
                        },
                    )
                task.save()
                account = Account.objects.get(user=user)
                Balance.objects.create(account=account, debit=task.price)
                AuditLog.objects.create(
                    user=user,
                    description=f"Assigned to task {task.public_id} with price: {task.fee}$. Account balance: {account.balance}$",
                )

            elif properties.content_type == Tracker.TASK_COMPLETED:
                user = AuthUser.objects.get(public_id=body["assignee"])
                task = Task.objects.get(public_id=body["public_id"])
                task.status = body["status"]
                task.fee = int(body["fee"])
                if version == "3":
                    task.jira_id = body["jira_id"]
                task.save()
                account = Account.objects.get(user=user)
                Balance.objects.create(account=account, credit=task.fee)
                AuditLog.objects.create(
                    user=user,
                    description=f"Completed task {task.public_id} with fee: {task.fee}$. Account balance: {account.balance}$",
                )

            logger.info("-" * 100)

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()
