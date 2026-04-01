from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..auth import verify_token
from ..utils.termux import clipboard_get, clipboard_set

router = APIRouter(prefix="/clipboard", tags=["clipboard"], dependencies=[Depends(verify_token)])


@router.get("")
async def get_clipboard():
    return {"content": await clipboard_get()}


class ClipboardSetRequest(BaseModel):
    text: str


@router.post("")
async def set_clipboard(req: ClipboardSetRequest):
    await clipboard_set(req.text)
    return {"set": True}
