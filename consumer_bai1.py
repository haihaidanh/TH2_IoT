"""
Bai 1 - Consumer
Lang nghe queue 'iot_lab_queue', in noi dung message va thoi diem nhan.
Chay lien tuc cho toi khi nhan Ctrl+C.

Chay:  python consumer_bai1.py
"""
import os
from datetime import datetime

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

QUEUE_NAME = "iot_lab_queue"


def on_message(channel, method, properties, body):
    print(f"Da nhan message: {body.decode('utf-8')}")
    print(f"Thoi gian nhan: {datetime.now().strftime('%H:%M:%S')}")
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
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

    print(f"[*] Dang cho message tu '{QUEUE_NAME}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Da dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
