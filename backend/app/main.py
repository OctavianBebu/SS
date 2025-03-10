from fastapi import FastAPI
from routes import images

app = FastAPI()

app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}
