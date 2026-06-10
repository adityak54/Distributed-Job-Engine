from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseJobHandler(ABC):
    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> None:
        """
        Executes the job logic. 
        If it raises an exception, the worker will catch it and mark the job FAILED.
        """
        pass