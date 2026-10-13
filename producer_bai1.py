
import os
import sys

import pika

STUDENT_NAME = "Nguyen Danh Hai"
STUDENT_ID = "B23DCCN274"

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

QUEUE_NAME = "iot_lab_queue"


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

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

    for i in range(1, count + 1):
        message = f"Xin chao tu ung dung Python AMQP - {STUDENT_ID} - {STUDENT_NAME}"
        if count > 1:
            message += f" (#{i})"
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"[x] Da gui: {message}")

    connection.close()


if __name__ == "__main__":
    main()
