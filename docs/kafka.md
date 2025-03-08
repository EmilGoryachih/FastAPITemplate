# Использование Kafka с FastAPI

## 1. Установка и запуск Kafka

### Установка локально (Linux)
#### Fedora:
```bash
sudo dnf install kafka -y
```
#### Ubuntu/Debian:
```bash
sudo apt install kafka -y
```

### Запуск Kafka в Docker
Создайте `docker-compose.yml`:
```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://localhost:9092"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```
Запустите Kafka:
```bash
docker-compose up -d
```
Проверьте работу:
```bash
docker logs kafka | grep "started"
```

---

## 2. Установка клиента Kafka для Python

```bash
pip install aiokafka
```

---

## 3. Конфигурация Kafka в FastAPI

### **Настройка продюсера (Producer)**
```python
from aiokafka import AIOKafkaProducer
import asyncio

async def send_message(topic: str, message: str):
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait(topic, message.encode('utf-8'))
    finally:
        await producer.stop()
```

### **Настройка консюмера (Consumer)**
```python
from aiokafka import AIOKafkaConsumer
import asyncio

async def consume_messages(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        group_id="my-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Получено сообщение: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()
```

---

## 4. Интеграция Kafka в FastAPI

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages("my_topic"))

@app.post("/send/")
async def send_kafka_message(msg: str):
    await send_message("my_topic", msg)
    return {"status": "sent"}
```

Запустите FastAPI:
```bash
uvicorn main:app --reload
```

Отправьте сообщение через HTTP-запрос:
```bash
curl -X POST "http://127.0.0.1:8000/send/" -H "Content-Type: application/json" -d '{"msg": "Hello Kafka!"}'
```

---

## 5. Расширенный функционал Kafka в FastAPI

### **Создание топиков вручную**
```bash
docker exec -it kafka kafka-topics --create --topic my_topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### **Балансировка нагрузки через Consumer Groups**
```python
consumer = AIOKafkaConsumer(
    "my_topic",
    bootstrap_servers='localhost:9092',
    group_id="worker-group"
)
```

### **Кеширование сообщений через Redis**
```python
from redis.asyncio import Redis

redis = Redis(host="localhost", port=6379)

async def consume_and_cache(topic: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id="my-group")
    await consumer.start()
    try:
        async for msg in consumer:
            await redis.setex(f"kafka:{topic}", 60, msg.value.decode('utf-8'))
    finally:
        await consumer.stop()
```

### **Мониторинг Kafka через UI**
```bash
docker run -d --name kafka-ui -p 8080:8080 -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=localhost:9092 provectuslabs/kafka-ui
```
Открыть в браузере: `http://localhost:8080`

---

## 6. Подключение к удалённому Kafka-брокеру

```python
producer = AIOKafkaProducer(bootstrap_servers='kafka.example.com:9092')
consumer = AIOKafkaConsumer("topic", bootstrap_servers='kafka.example.com:9092', group_id="my-group")
```

---

## 7. Заключение

- Kafka отлично подходит для асинхронных событий в FastAPI.
- Можно использовать **балансировку** через группы консюмеров.
- Можно **кешировать** данные через Redis.
- Мониторинг через Kafka UI упрощает администрирование.

Готово к продакшену! 🚀
