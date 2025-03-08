# Использование Redis с FastAPI

## 1. Установка и запуск Redis

### Установка Redis
#### Fedora:
```bash
sudo dnf install redis -y
```
#### Ubuntu/Debian:
```bash
sudo apt install redis -y
```

### Запуск Redis как сервиса:
```bash
sudo systemctl start redis
sudo systemctl enable redis
```

### Проверка работы:
```bash
redis-cli ping  # Должен ответить "PONG"
```

### Запуск Redis в Docker:
```bash
docker run -d --name redis -p 6379:6379 redis:latest
```

---

## 2. Подключение FastAPI к Redis

```python
from redis.asyncio import Redis

redis = Redis(host="localhost", port=6379, decode_responses=True)
```

Если Redis работает в Docker:
```python
redis = Redis(host="redis", port=6379, decode_responses=True)
```

---

## 3. Кеширование данных и запросов

```python
async def get_from_cache(key: str):
    return await redis.get(key)

async def set_to_cache(key: str, value: str, ttl: int = 60):
    await redis.setex(key, ttl, value)
```

### Кеширование эндпоинтов с `fastapi-cache2`
```bash
pip install fastapi-cache2 redis
```
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/expensive")
@cache(expire=60)
async def expensive_operation():
    return {"data": "Expensive computation"}
```

---

## 4. Pub/Sub (Система сообщений и событий)

```python
async def listen_to_redis():
    pubsub = redis.pubsub()
    await pubsub.subscribe("my_channel")
    async for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Получено сообщение: {message['data']}")
```
```python
@app.post("/publish/")
async def publish_message(message: str):
    await redis.publish("my_channel", message)
    return {"status": "Message sent"}
```

---

## 5. Очереди задач (Job Queue)

```bash
pip install rq
```
```python
import redis
from rq import Queue

redis_conn = redis.Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

job = queue.enqueue(lambda x: x * 2, 5)
```

---

## 6. Блокировки и мьютексы

```bash
pip install redlock-py
```
```python
from redlock import Redlock

dlm = Redlock([{ "host": "localhost", "port": 6379, "db": 0 }])
lock = dlm.lock("resource_lock", 1000)  # 1000 мс

dlm.unlock(lock)
```

---

## 7. Хранение сессий и JWT-токенов

```python
import jwt, datetime
SECRET_KEY = "your-secret-key"

async def create_token(user_id: str):
    payload = {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    await redis.setex(f"token:{user_id}", 86400, token)
    return token
```

---

## 8. Rate Limiting (Ограничение запросов per user/IP)

```python
async def rate_limiter(request):
    ip = request.client.host
    key = f"rate_limit:{ip}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, 60)
    if current > 10:
        raise HTTPException(status_code=429, detail="Too many requests")
```

---

## 9. Хранение JSON-данных (RedisJSON)

```bash
docker run -d --name redis -p 6379:6379 redis/redis-stack
```
```python
await redis.json().set("user:123", "$", {"name": "Alice", "age": 30})
user = await redis.json().get("user:123", "$")