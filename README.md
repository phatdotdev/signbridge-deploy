# 🧠 Sign Recognition System - FastAPI + React + Celery + Redis + PostgreSQL

Ứng dụng fullstack gồm:
- **Backend:** FastAPI (Python 3.11)
- **Frontend:** React (Node 18)
- **Message Queue:** Celery + Redis
- **Database:** PostgreSQL
- **Triển khai:** Docker Compose

---

## 🗂️ Cấu trúc thư mục

1️⃣ Clone repository

2️⃣ Tạo file .env

# Backend
BACKEND_PORT=8000
DATABASE_URL=postgresql://signuser:signpass@postgres:5432/signdb

# Celery
REDIS_URL=redis://redis:6379/0

# Frontend
VITE_API_URL=http://localhost:8000

# PostgreSQL (container)
POSTGRES_USER=signuser
POSTGRES_PASSWORD=signpass
POSTGRES_DB=signdb

# ===============================
# ⚙️ BACKEND CONFIGURATION
# ===============================
DATABASE_URL=postgresql://signuser:signpass@postgres:5432/signdb

# ===============================
# 🧮 CELERY CONFIGURATION
# ===============================
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# ===============================
# 💾 STORAGE CONFIGURATION
# ===============================
STORAGE_PATH=/app/storage

# ===============================
# ☁️ MINIO CONFIGURATION
# ===============================
# MinIO dùng để lưu trữ file, hình ảnh, dataset,...
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minio-access-key
MINIO_SECRET_KEY=minio-secret-key
MINIO_BUCKET=sign-dataset

# ===============================
# 🔐 TOKEN SECRETS
# ===============================
ACCESS_TOKEN_SECRET=your-access-token-secret
REFRESH_TOKEN_SECRET=your-refresh-token-secret

# ===============================
# 🌐 FRONTEND CONFIGURATION
# ===============================
REACT_APP_API_URL=http://localhost:8000


3️⃣ Build & Run Docker Compose

docker compose up --build
