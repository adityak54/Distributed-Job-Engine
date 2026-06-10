import time
from src.handlers.base import BaseJobHandler

class GenerateReportHandler(BaseJobHandler):
    def execute(self, payload: dict) -> None:
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("user_id is required in the payload")
            
        print(f"[GenerateReport] Starting report generation for user: {user_id}")
        
        # Simulate heavy I/O or CPU work
        time.sleep(3) 
        
        print(f"[GenerateReport] Successfully generated report for user: {user_id}")