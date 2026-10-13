# Thuc hanh Python AMQP (Bai 1, 2, 3)

## Broker su dung
RabbitMQ (AMQP 0-9-1) + thu vien Python `pika`.
Mac dinh `localhost:5672`, user/pass `guest/guest`. Doi bang bien moi truong
`RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASS`.

## Chuan bi
```bash
pip install pika
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
Bai 1: sua `STUDENT_NAME`, `STUDENT_ID` o dau file `producer_bai1.py`.

## Cach chay (moi lenh o 1 terminal rieng, Ctrl+C de dung)

### Bai 1
```bash
python consumer_bai1.py
python producer_bai1.py          # hoac: python producer_bai1.py 5  (gui 5 message)
```
Ket qua: consumer in `Da nhan message: ...` va `Thoi gian nhan: HH:MM:SS`.

### Bai 2
```bash
python monitor_consumer_bai2.py
python sensor_producer_bai2.py
```
Ket qua: producer gui JSON 3 cam bien moi 3 giay; consumer in Device/Temperature/Humidity
va `CANH BAO: Nhiet do cao` (nhiet do > 35), `CANH BAO: Do am thap` (do am < 40).

### Bai 3
**Chay 2 consumer truoc, producer sau** (de queue da duoc bind khi message duoc gui):
```bash
python warning_consumer_bai3.py
python critical_consumer_bai3.py
python alert_producer_bai3.py
```
Ket qua: message `info` khong consumer nao nhan; `warning` chi `warning_queue` nhan;
`critical` chi `critical_queue` nhan.

## Ket qua dat duoc
- Bai 1: ket noi broker, gui/nhan message qua queue `iot_lab_queue`, hien thi noi dung va thoi gian nhan.
- Bai 2: payload JSON, gui tuan hoan 3 giay, consumer phat hien canh bao dung.
- Bai 3: tao direct exchange `iot_alert_exchange`, bind dung routing key, phan phoi message dung noi nhan.
