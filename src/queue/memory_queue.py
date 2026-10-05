import queue
from src.queue.base import BaseQueue


class MemoryQueue(BaseQueue):
    """In-memory queue for dev/testing. Not suitable for multi-process workers."""

    def __init__(self):
        self._queue: queue.Queue[str] = queue.Queue()

    def enqueue(self, job_id: str) -> None:
        self._queue.put(job_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None
