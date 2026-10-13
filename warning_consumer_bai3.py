"""
Bai 3 - Warning Consumer
Tao queue 'warning_queue', bind vao exchange 'iot_alert_exchange' voi
routing key 'warning' va chi nhan canh bao muc warning.

Chay:  python warning_consumer_bai3.py
"""
import os

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "warning_queue"
ROUTING_KEY = "warning"


def on_message(channel, method, properties, body):
    print(f"[{QUEUE_NAME}] Da nhan: {body.decode('utf-8')}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
    )
    try:
        connection = pika.BlockingConnection(params)
    except pika.exceptions.AMQPConnectionError:
        print(f"Khong ket noi duoc RabbitMQ tai {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return

    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

    print(f"[*] '{QUEUE_NAME}' dang cho canh bao muc '{ROUTING_KEY}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Da dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
