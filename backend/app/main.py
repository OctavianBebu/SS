from fastapi import FastAPI
from app.routes import images, auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if your frontend is hosted elsewhere
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}
