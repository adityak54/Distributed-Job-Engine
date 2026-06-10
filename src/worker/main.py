import os
import redis
from src.worker.executor import process_job

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def start_worker():
    print("Worker started. Listening for jobs on 'job_queue'...")
    while True:
        try:
            # blpop blocks the loop until a job enters the queue. 
            # It prevents the worker from maxing out your CPU.
            result = redis_client.blpop("job_queue", timeout=0)
            
            if result:
                queue_name, job_id = result
                print(f"\n--- Picked up Job ID: {job_id} ---")
                process_job(job_id)
                
        except Exception as e:
            print(f"Worker encountered an error: {e}")

if __name__ == "__main__":
    start_worker()