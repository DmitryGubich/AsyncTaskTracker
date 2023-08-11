import pika


def produce(payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="auth", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="auth",
        body=payload,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    print(f" [x] Sent {payload}")
    connection.close()
