from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.termux import get_volume, set_volume

router = APIRouter(prefix="/volume", tags=["volume"], dependencies=[Depends(verify_token)])
VALID_STREAMS = ["music", "call", "ring", "alarm", "notification", "system"]


@router.get("")
async def get_vol():
    return await get_volume()


class VolumeSetRequest(BaseModel):
    stream: str
    value: int = Field(..., ge=0, le=15)


@router.post("")
async def set_vol(req: VolumeSetRequest):
    if req.stream not in VALID_STREAMS:
        raise HTTPException(status_code=400, detail=f"Invalid stream. Use: {VALID_STREAMS}")
    return {"stream": req.stream, "value": req.value, "result": await set_volume(req.stream, req.value)}
