from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth import sign_up, sign_in

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(req: AuthRequest):
    try:
        response = await sign_up(req.email, req.password)
        return {"message": "Check your email to confirm your account!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login")
async def login(req: AuthRequest):
    try:
        response = await sign_in(req.email, req.password)
        return {
            "access_token": response.session.access_token,
            "user": response.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")