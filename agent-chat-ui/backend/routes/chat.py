from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    # Stubbed reply — replace with actual LLM logic later
    reply = f"You said: {message}"

    return JSONResponse(content={"reply": reply})

