from fastapi import APIRouter, Depends
from typing import Optional
from app.worker import celery_app
from app.core.oauth2 import get_current_admin

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job_status(job_id: str, current_admin = Depends(get_current_admin)):
    """
    Query job status from Celery
    """
    from celery.result import AsyncResult
    result = AsyncResult(job_id, app=celery_app)

    response = {
        "job_id": job_id,
        "status": result.status,   # PENDING, STARTED, SUCCESS, FAILURE, RETRY
        "result": result.result if result.successful() else None,
        "traceback": str(result.traceback) if result.failed() else None
    }
    return response


@router.get("/")
def list_jobs(limit: int = 10, current_admin = Depends(get_current_admin)):
    """
    ⚠️ Celery không lưu job history mặc định.
    Để list nhiều job, bạn cần kết hợp Redis backend hoặc DB backend.
    Ở đây chỉ demo nên chỉ trả thông báo.
    """
    return {"message": f"Listing last {limit} jobs not implemented (use DB backend)."}
