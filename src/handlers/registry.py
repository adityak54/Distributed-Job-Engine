from src.handlers.base import JobHandler


class HandlerRegistry:
    def __init__(self):
        self._handlers: dict[str, JobHandler] = {}

    def register(self, handler: JobHandler) -> None:
        self._handlers[handler.name] = handler

    def get(self, name: str) -> JobHandler:
        handler = self._handlers.get(name)
        if handler is None:
            raise KeyError(f"No handler registered for job type: '{name}'")
        return handler

    def list_handlers(self) -> list[str]:
        return list(self._handlers.keys())


registry = HandlerRegistry()
