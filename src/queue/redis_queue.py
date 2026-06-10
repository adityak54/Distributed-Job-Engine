import os
import redis

# Connect to the Redis container we spun up earlier
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def enqueue_job(job_id: str):
    # Pushes the job ID to the right side of a Redis list named 'job_queue'
    redis_client.rpush("job_queue", job_id)