from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime
from database import SessionLocal
from models import Image

router = APIRouter()

UPLOAD_DIR = "uploaded_images"  # Directory for storing uploaded images
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image(filename=file.filename, filepath=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)

    return {"message": "File uploaded successfully", "image_id": image.id}
