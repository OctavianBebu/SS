from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
import shutil
import os
from app.database import SessionLocal
from app.models import Image, User
from fastapi.security import OAuth2PasswordBearer
from app.security import decode_token

router = APIRouter()

UPLOAD_DIR = "uploaded_images"  # Directory for storing uploaded images
os.makedirs(UPLOAD_DIR, exist_ok=True)

# OAuth2 scheme pentru autentificare
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Conectare la baza de date
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funcție pentru a obține utilizatorul curent
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint protejat pentru upload imagini
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image(filename=file.filename, filepath=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)

    return {"message": f"File uploaded successfully by {current_user.username}", "image_id": image.id}
