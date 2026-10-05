from abc import ABC, abstractmethod


class JobHandler(ABC):
    """Base class for all job handlers. Subclass and implement execute()."""

    name: str

    @abstractmethod
    def execute(self, payload: dict) -> dict:
        """Run the job logic. Returns a result dict on success, raises on failure."""
        ...

    def validate(self, payload: dict) -> bool:
        """Optional payload validation. Override to add checks."""
        return True
