from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.summarize import router
from app.routes.auth import router as auth_router

app = FastAPI(title="AI PDF Summarizer API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/auth")
def auth_page():
    return FileResponse("static/auth.html")

app.include_router(router)
app.include_router(auth_router)