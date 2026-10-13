"""
Bai 2 - Sensor Producer
Mo phong cac cam bien IoT gui du lieu moi truong (JSON) moi 3 giay
vao queue 'sensor_data_queue' thong qua AMQP (RabbitMQ).

Chay:  python sensor_producer_bai2.py
Dung:  Ctrl+C
"""
import json
import os
import random
import time
from datetime import datetime

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

QUEUE_NAME = "sensor_data_queue"
INTERVAL_SECONDS = 3
DEVICES = ["sensor01", "sensor02", "sensor03"]  # mo rong: nhieu cam bien


def generate_payload(device_id: str) -> dict:
    """Sinh du lieu ngau nhien cho mot cam bien."""
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(25.0, 40.0), 1),
        "humidity": round(random.uniform(30.0, 80.0), 1),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # mo rong
    }


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials
    )

    try:
        connection = pika.BlockingConnection(params)
    except pika.exceptions.AMQPConnectionError:
        print(f"Khong ket noi duoc RabbitMQ tai {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    print(f"[*] Da ket noi {RABBITMQ_HOST}. Gui du lieu moi {INTERVAL_SECONDS}s. Ctrl+C de dung.")

    try:
        while True:
            for device_id in DEVICES:
                payload = generate_payload(device_id)
                channel.basic_publish(
                    exchange="",
                    routing_key=QUEUE_NAME,
                    body=json.dumps(payload),
                    properties=pika.BasicProperties(
                        content_type="application/json",
                        delivery_mode=2,  # message ben vung
                    ),
                )
                print(f"[x] Da gui: {json.dumps(payload)}")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n[!] Da dung producer.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
