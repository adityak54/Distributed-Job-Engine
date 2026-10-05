from src.worker.retry import get_backoff_delay


def test_exponential_backoff():
    assert get_backoff_delay(0) == 2.0   # 2 * 2^0
    assert get_backoff_delay(1) == 4.0   # 2 * 2^1
    assert get_backoff_delay(2) == 8.0   # 2 * 2^2
    assert get_backoff_delay(3) == 16.0  # 2 * 2^3


def test_backoff_capped():
    assert get_backoff_delay(10, cap=60.0) == 60.0
