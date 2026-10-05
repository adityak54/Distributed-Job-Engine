from abc import ABC, abstractmethod


class BaseQueue(ABC):
    @abstractmethod
    def enqueue(self, job_id: str) -> None: ...

    @abstractmethod
    def dequeue(self, timeout: int = 0) -> str | None: ...
