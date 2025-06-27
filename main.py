from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.health import router as health_router

app = FastAPI()

# Allow requests from iOS app (important for testing on simulator/device)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your iOS app domain here if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the health routes
app.include_router(health_router, prefix="/health", tags=["Health"])

# Optional: root route to check if server is alive
@app.get("/")
def read_root():
    return {"message": "HealthMY FastAPI backend is running"}