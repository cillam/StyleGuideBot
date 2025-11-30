from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/health")
def read_health_status():
    return {"status": "healthy"}

