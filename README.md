# Thực hành lập trình Python với giao thức AMQP


## 1. Môi trường

| Thành phần | Ghi chú |
|---|---|
| Python | 3.x |
| Thư viện | `pika` |
| Broker | RabbitMQ (AMQP 0-9-1), cài trực tiếp trên máy hoặc dùng broker chung của lớp |
| Công cụ | VS Code / terminal |

**Cài thư viện:**

```bash
python -m pip install pika
```

**Kết nối mặc định:** `localhost:5672`, tài khoản `guest` / `guest`.
Nếu dùng broker khác, đặt các biến môi trường `RABBITMQ_HOST`, `RABBITMQ_PORT`,
`RABBITMQ_USER`, `RABBITMQ_PASS`.

```powershell
# Windows PowerShell
$env:RABBITMQ_HOST = "192.168.1.10"
```

## 2. Cấu trúc thư mục

```
full/
├── producer_bai1.py            # Bài 1 – gửi message
├── consumer_bai1.py            # Bài 1 – nhận message
├── sensor_producer_bai2.py     # Bài 2 – cảm biến gửi dữ liệu JSON
├── monitor_consumer_bai2.py    # Bài 2 – giám sát và cảnh báo
├── alert_producer_bai3.py      # Bài 3 – gửi cảnh báo qua exchange
├── warning_consumer_bai3.py    # Bài 3 – nhận cảnh báo warning
├── critical_consumer_bai3.py   # Bài 3 – nhận cảnh báo critical
└── README.md
```

## 3. Hướng dẫn chạy

Mỗi lệnh chạy trong **một terminal riêng**. Nhấn `Ctrl+C` để dừng.
Đảm bảo RabbitMQ đang chạy trước khi bắt đầu.

### Bài 1 – Gửi và nhận message cơ bản

Queue: `iot_lab_queue`. Mở file `producer_bai1.py`
và sửa `STUDENT_NAME`, `STUDENT_ID` thành thông tin của bạn.

```bash
python consumer_bai1.py
python producer_bai1.py        # gửi 1 message
python producer_bai1.py 5      # gửi 5 message liên tiếp
```

Kết quả mong đợi ở consumer:

```
Da nhan message: Xin chao tu ung dung Python AMQP - B21xxxx - Nguyen Van A
Thoi gian nhan: 14:05:21
```

### Bài 2 – Mô phỏng cảm biến IoT

Queue: `sensor_data_queue`. Producer mô phỏng 3 cảm biến (`sensor01`–`sensor03`),
gửi dữ liệu mỗi 3 giây dưới dạng JSON, nhiệt độ ngẫu nhiên 25–40, độ ẩm ngẫu nhiên 30–80.

```bash
python monitor_consumer_bai2.py
python sensor_producer_bai2.py
```

Ví dụ payload:

```json
{"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-13 19:35:01"}
```

Kết quả mong đợi ở consumer:

```
Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

Điều kiện cảnh báo: nhiệt độ > 35 hoặc độ ẩm < 40.

### Bài 3 – Direct exchange và routing key

Exchange: `iot_alert_exchange` (kiểu `direct`).

| Routing key | Queue nhận | Consumer |
|---|---|---|
| `warning` | `warning_queue` | `warning_consumer_bai3.py` |
| `critical` | `critical_queue` | `critical_consumer_bai3.py` |
| `info` | không có | không consumer nào nhận |

> **Lưu ý:** chạy 2 consumer **trước**, producer **sau**, để các queue đã được bind
> vào exchange khi message được gửi.

```bash
python warning_consumer_bai3.py
python critical_consumer_bai3.py
python alert_producer_bai3.py
```

Kết quả mong đợi:

```
[warning_queue]  Da nhan: Nhiet do phong may vuot nguong warning
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

## 4. Kết quả đạt được

- **Bài 1:** kết nối được broker, gửi và nhận message qua queue `iot_lab_queue`,
  hiển thị nội dung và thời điểm nhận.
- **Bài 2:** payload đúng định dạng JSON, gửi tuần hoàn mỗi 3 giây, consumer phân tích
  dữ liệu và cảnh báo đúng theo ngưỡng.
- **Bài 3:** tạo direct exchange, bind đúng routing key, message được phân phối chính xác
  tới từng queue.

