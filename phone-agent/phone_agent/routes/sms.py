from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.termux import sms_list, sms_send

router = APIRouter(prefix="/sms", tags=["sms"], dependencies=[Depends(verify_token)])


@router.get("")
async def list_sms(limit: int = Query(default=10, ge=1, le=100)):
    messages = await sms_list(limit)
    return {"messages": messages, "count": len(messages)}


class SmsSendRequest(BaseModel):
    number: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


@router.post("")
async def send_sms(req: SmsSendRequest):
    result = await sms_send(req.number, req.body)
    return {"sent": True, "result": result}
