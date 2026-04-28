import os
from supabase import create_client, Client

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_PUBLISHABLE_KEY")
)

async def sign_up(email: str, password: str):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })
    return response

async def sign_in(email: str, password: str):
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    return response

async def get_user(token: str):
    response = supabase.auth.get_user(token)
    return response.user

async def save_summary(user_id: str, data: dict):
    supabase.table("summaries").insert({
        "user_id": user_id,
        **data
    }).execute()

async def get_user_summaries(user_id: str):
    response = supabase.table("summaries")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .execute()
    return response.data