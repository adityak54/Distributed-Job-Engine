import math
import time
import logging

logger = logging.getLogger(__name__)

BASE_DELAY = 2  # seconds


def get_backoff_delay(retry_count: int, base: float = BASE_DELAY, cap: float = 60.0) -> float:
    """Exponential backoff: base * 2^retry_count, capped at `cap` seconds."""
    return min(base * math.pow(2, retry_count), cap)


def wait_for_retry(retry_count: int) -> None:
    delay = get_backoff_delay(retry_count)
    logger.info(f"Backing off for {delay:.1f}s before retry #{retry_count + 1}")
    time.sleep(delay)
