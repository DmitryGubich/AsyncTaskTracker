import time
from os import environ
from sys import path

import django
import pika

path.append("/Users/dmitry/Projects/UberPopugInc/tracker/app/settings.py")
environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
from tracker.models import AuthUser

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    event = body.decode()
    print(f" [x] Received {event}")
    user = AuthUser.objects.create(
        public_id=event.get("public_id"), role=event.get("role")
    )
    user.save()
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="auth", on_message_callback=callback)

channel.start_consuming()
