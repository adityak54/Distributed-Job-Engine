import redis
from src.queue.base import BaseQueue

QUEUE_KEY = "job_engine:jobs"


class RedisQueue(BaseQueue):
    def __init__(self, redis_url: str):
        self._client = redis.from_url(redis_url)

    def enqueue(self, job_id: str) -> None:
        self._client.rpush(QUEUE_KEY, job_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        # BLPOP blocks until an item is available or timeout is reached
        result = self._client.blpop(QUEUE_KEY, timeout=timeout)
        if result is None:
            return None
        # result is (key, value) tuple
        return result[1].decode() if isinstance(result[1], bytes) else result[1]
