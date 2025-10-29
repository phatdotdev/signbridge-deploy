from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import os
import shutil
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path


from app.processing import storage_utils as su
from ..core.oauth2 import get_current_user, get_current_admin, check_resource_owner
from ..db import get_db, User

router = APIRouter(prefix="/dataset", tags=["dataset"])
DATASET_PATH = Path("dataset/features")

# ---- Models ----
class LabelOut(BaseModel):
    class_idx: int
    label_original: str
    slug: str
    folder_name: str
    created_at: str
    dataset_version: str
    notes: str

class SampleOut(BaseModel):
    sample_id: str
    class_idx: int
    folder_name: str
    file: str
    user: str
    session_id: str
    frames: str
    duration: str
    source: str
    created_at: str


# ---- Endpoints ----



# admin
@router.post("/labels", response_model=LabelOut)
def create_label(label: str = Form(...), 
                 notes: str = Form(""), 
                 version: str = Form("v1"),
                 admin_user: User = Depends(get_current_admin)): 
    class_idx, folder = su.register_label(label, notes=notes, dataset_version=version)
    labels = su.read_csv(su.LABELS_CSV)
    new_label = next(r for r in labels if int(r["class_idx"]) == class_idx)
    return new_label


# admin, user
@router.get("/labels", response_model=List[LabelOut])
def list_labels(current_user: User = Depends(get_current_user)):
    return su.read_csv(su.LABELS_CSV)

#admin
@router.post("/labels/merge")
def merge_labels(src_class_idx: int = Form(...), dst_class_idx: int = Form(...),  admin_user: User = Depends(get_current_admin)):
    ok = su.merge_labels(src_class_idx, dst_class_idx)
    return {"status": "success" if ok else "failed"}

# admin - Xóa label
@router.delete("/labels/{class_idx}")
def delete_label(class_idx: int, admin_user: User = Depends(get_current_admin)):
    """
    Xóa label theo class_idx.
    Lưu ý: Nên kiểm tra xem có samples nào đang dùng label này không.
    """
    labels = su.read_csv(su.LABELS_CSV)
    label = next((r for r in labels if int(r["class_idx"]) == class_idx), None)
    
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    
    # Kiểm tra xem có samples nào đang dùng label này không
    samples = su.read_csv(su.SAMPLES_CSV)
    samples_with_label = [s for s in samples if int(s.get("class_idx", -1)) == class_idx]
    
    if samples_with_label:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete label. {len(samples_with_label)} samples are using this label"
        )
    
    # Xóa label khỏi CSV
    labels = [r for r in labels if int(r["class_idx"]) != class_idx]
    
    # Ghi lại file CSV
    import csv
    with open(su.LABELS_CSV, 'w', newline='', encoding='utf-8') as f:
        if labels:
            writer = csv.DictWriter(f, fieldnames=labels[0].keys())
            writer.writeheader()
            writer.writerows(labels)
    
    # Xóa thư mục nếu tồn tại
    folder_path = os.path.join("dataset/features", label["folder_name"])
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    return {"status": "success", "message": f"Label {class_idx} deleted"}

# admin - Sửa label
@router.put("/labels/{class_idx}", response_model=LabelOut)
def update_label(
    class_idx: int,
    label: str = Form(None),
    notes: str = Form(None),
    admin_user: User = Depends(get_current_admin)
):
    """
    Cập nhật thông tin label.
    Chỉ cho phép sửa label_original và notes, không sửa class_idx.
    """
    labels = su.read_csv(su.LABELS_CSV)
    label_index = next((i for i, r in enumerate(labels) if int(r["class_idx"]) == class_idx), None)
    
    if label_index is None:
        raise HTTPException(status_code=404, detail="Label not found")
    
    # Cập nhật các trường được cho phép
    if label is not None:
        labels[label_index]["label_original"] = label
        # Cập nhật slug nếu label thay đổi
        import re
        new_slug = re.sub(r'[^a-z0-9]+', '_', label.lower()).strip('_')
        labels[label_index]["slug"] = new_slug
    
    if notes is not None:
        labels[label_index]["notes"] = notes
    
    # Ghi lại file CSV
    import csv
    with open(su.LABELS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=labels[0].keys())
        writer.writeheader()
        writer.writerows(labels)
    
    return labels[label_index]




# User chỉ xem, xóa của mình
# admin xem, xóa tất cả
@router.get("/samples", response_model=List[SampleOut])
def list_samples(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    samples = su.read_csv(su.SAMPLES_CSV)

    if current_user.role != "admin":
        samples = [s for s in samples if s.get("user") == current_user.username]
    return samples


# User chỉ xem của mình
@router.get("/samples/{sample_id}/data")
def get_sample_data(sample_id: str, current_user: User = Depends(get_current_user)):
   
    samples = su.read_csv(su.SAMPLES_CSV)
    sample = next((s for s in samples if s["sample_id"] == sample_id), None)
   
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    # Kiểm tra quyền
    check_resource_owner(sample["user"], current_user)

    """
    Trả về file npz/json của sample_id
    """
    base_dir = "dataset/features"
    # giả sử trong samples.csv có file_path, bạn sẽ lookup từ đó
    import csv
    samples_file = os.path.join(base_dir, "samples.csv")

    with open(samples_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["sample_id"] == sample_id:
                file_path = row["file_path"]
                return FileResponse(file_path, media_type="application/octet-stream")

    return {"error": "Sample not found"}

# user, admin
@router.post("/samples/add")
def add_sample(
    class_idx: int = Form(...),
    user: str = Form(""),
    session_id: str = Form(""),
    frames: int = Form(0),
    duration: float = Form(0.0),
    source: str = Form("video"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # tìm folder theo class_idx
    labels = su.read_csv(su.LABELS_CSV)
    label = next((r for r in labels if int(r["class_idx"]) == class_idx), None)
    if not label:
        return {"status": "failed", "reason": "label not found"}
    folder = label["folder_name"]

    # lưu file upload tạm thời
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # đọc npz nếu cần, hoặc giả định file đã là npz chuẩn
    if file.filename.endswith(".npz"):
        seq = np.load(tmp_path)["sequence"]
    else:
        # fallback: random (chỉ demo)
        seq = np.random.rand(60, 1605)

    os.remove(tmp_path)

    # save sample
    metadata = {"user": user, "session_id": session_id, "frames": frames, "duration": duration, "source": source}
    path = su.save_sample(seq, class_idx, folder, metadata=metadata)
    return {"status": "ok", "path": path}
# ...existing code...

@router.get("/sessions")
def list_sessions(
    user: str = "", 
    label: str = "", 
    date: str = "",
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách sessions từ samples.csv
    """
    try:
        # Đọc samples.csv
        samples = su.read_csv(su.SAMPLES_CSV)
        
        if not samples:
            return []
        
        # Convert sang DataFrame
        df = pd.DataFrame(samples)
        
        # User chỉ xem của mình
        if current_user.role != "admin":
            df = df[df["user"] == current_user.username]
        else:
            # Admin có thể filter theo user
            if user:
                df = df[df["user"] == user]
        
        # Filter theo label (dùng class_idx hoặc folder_name)
        if label:
            df = df[df["folder_name"].str.contains(label, case=False, na=False)]
        
        # Filter theo date (dùng created_at)
        if date:
            df = df[df["created_at"].str.startswith(date, na=False)]
        
        # Group theo session_id
        sessions = []
        if "session_id" in df.columns:
            for sid, group in df.groupby("session_id"):
                # Lấy thông tin labels từ folder_name hoặc class_idx
                labels = list(group["folder_name"].unique()) if "folder_name" in group.columns else []
                
                sessions.append({
                    "session_id": sid,
                    "user": group["user"].iloc[0] if "user" in group.columns else "",
                    "labels": labels,
                    "samples_count": len(group),
                    "created_at": group["created_at"].iloc[0] if "created_at" in group.columns else "",
                })
        
        return sessions
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="samples.csv not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading sessions: {str(e)}")