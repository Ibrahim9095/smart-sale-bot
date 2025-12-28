from fastapi import APIRouter
from app.storage.memory import get_messages

router = APIRouter()

@router.get("/chat")
def read_chat():
    return get_messages()