from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dataset, upload, jobs, users, auth
from app.db import init_db

app = FastAPI(title="Sign Dataset Backend")

origins = os.getenv("CORS_ORIGINS", "").split(",")
print(origins)
# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init DB tables (dev). In prod, use migrations (alembic).
@app.on_event("startup")
def startup():
    init_db()

app.include_router(dataset.router)
app.include_router(upload.router)
app.include_router(jobs.router)
app.include_router(users.router)
app.include_router(auth.router)