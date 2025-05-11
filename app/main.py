# sim_post_cap_backend/app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="SimPostCap Backend API",
    description="API for simulating post-capitalist scenarios.",
    version="0.0.1",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to SimPostCap API!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}