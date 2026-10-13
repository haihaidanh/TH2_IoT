"""
Bai 2 - Monitoring Consumer
Nhan du lieu tu queue 'sensor_data_queue', phan tich JSON va in canh bao:
  - nhiet do > 35  -> "CANH BAO: Nhiet do cao"
  - do am   < 40   -> "CANH BAO: Do am thap"

Chay:  python monitor_consumer_bai2.py
Dung:  Ctrl+C
"""
import json
import os

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

QUEUE_NAME = "sensor_data_queue"
TEMP_THRESHOLD = 35
HUMIDITY_THRESHOLD = 40


def on_message(channel, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        device_id = data["device_id"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as err:
        print(f"[!] Message khong hop le, bo qua: {err}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return

    print("-" * 40)
    print(f"Device: {device_id}")
    print(f"Temperature: {temperature}")
    print(f"Humidity: {humidity}")
    if "timestamp" in data:
        print(f"Time: {data['timestamp']}")

    if temperature > TEMP_THRESHOLD:
        print("CANH BAO: Nhiet do cao")
    if humidity < HUMIDITY_THRESHOLD:
        print("CANH BAO: Do am thap")

    channel.basic_ack(delivery_tag=method.delivery_tag)


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
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

    print(f"[*] Dang cho du lieu tu '{QUEUE_NAME}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Da dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
