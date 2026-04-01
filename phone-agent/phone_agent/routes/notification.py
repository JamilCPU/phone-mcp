from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.termux import send_notification

router = APIRouter(prefix="/notification", tags=["notification"], dependencies=[Depends(verify_token)])


class NotificationRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = ""
    id: int = 1


@router.post("")
async def notify(req: NotificationRequest):
    result = await send_notification(req.title, req.content, req.id)
    return {"sent": True, "result": result}
