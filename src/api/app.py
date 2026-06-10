from fastapi import FastAPI
from src.api.routes import jobs

app = FastAPI(title="Job Execution Engine API", version="1.0.0")

# Register the routes
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "api"}