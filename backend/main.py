from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import models, database
from backend.routes import  auth, device, backup

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router)
app.include_router(device.router)
app.include_router(backup.router)
