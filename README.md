# 🧠 Sign Recognition System

**Fullstack ứng dụng nhận diện ngôn ngữ ký hiệu** sử dụng **FastAPI + React + Celery + Redis + PostgreSQL + MinIO**, được đóng gói hoàn toàn bằng **Docker Compose**.

---

## 🚀 Tính năng chính

- **Backend mạnh mẽ** với FastAPI (Python 3.11)
- **Giao diện người dùng hiện đại** bằng React (Node 18)
- **Xử lý tác vụ nền** bằng Celery + Redis
- **Lưu trữ dữ liệu** với PostgreSQL
- **Quản lý file & dataset** qua MinIO (S3-compatible)
- **Triển khai dễ dàng** với Docker Compose
- **Hỗ trợ upload, xử lý video/hình ảnh, nhận diện ký hiệu**

---

## 🗂️ Cấu trúc thư mục

```bash
project-root/
├── backend/              # FastAPI backend
│   ├── app/              # Source code
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
│
├── frontend/             # React frontend
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── ...
│
├── dataset/              # Thư mục lưu dataset mẫu (mounted)
├── docker-compose.yml   # Cấu hình toàn bộ hệ thống
├── .env                  # Biến môi trường
└── README.md             # Tài liệu hướng dẫn

file .env
# Backend
BACKEND_PORT=8000
DATABASE_URL=postgresql://signuser:signpass@postgres:5432/signdb

# Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Frontend
VITE_API_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000

# PostgreSQL
POSTGRES_USER=signuser
POSTGRES_PASSWORD=signpass
POSTGRES_DB=signdb

# Storage
STORAGE_PATH=/app/storage

# MinIO (Object Storage)
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minio-access-key
MINIO_SECRET_KEY=minio-secret-key
MINIO_BUCKET=sign-dataset

# JWT Token Secrets
ACCESS_TOKEN_SECRET=your-super-secret-access-token-key-here
REFRESH_TOKEN_SECRET=your-super-secret-refresh-token-key-here

Khởi chạy hệ thống
docker compose up --build
