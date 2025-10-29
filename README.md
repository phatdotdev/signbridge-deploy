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
