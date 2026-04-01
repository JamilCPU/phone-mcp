import base64
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.termux import torch, vibrate, tts_speak, camera_photo

router = APIRouter(prefix="/media", tags=["media"], dependencies=[Depends(verify_token)])


class TorchRequest(BaseModel):
    on: bool


@router.post("/torch")
async def toggle_torch(req: TorchRequest):
    return {"torch": req.on, "result": await torch(req.on)}


class VibrateRequest(BaseModel):
    duration_ms: int = Field(default=500, ge=100, le=10000)


@router.post("/vibrate")
async def do_vibrate(req: VibrateRequest):
    return {"vibrated": True, "duration_ms": req.duration_ms, "result": await vibrate(req.duration_ms)}


class TtsRequest(BaseModel):
    text: str = Field(..., min_length=1)
    language: str = "en"


@router.post("/tts")
async def text_to_speech(req: TtsRequest):
    return {"spoken": True, "result": await tts_speak(req.text, req.language)}


class CameraRequest(BaseModel):
    camera_id: int = Field(default=0, ge=0, le=3)


@router.post("/camera")
async def take_photo(req: CameraRequest):
    data = await camera_photo(req.camera_id)
    if data is None:
        raise HTTPException(status_code=503, detail="Camera capture failed. Ensure termux-api camera permission is granted.")
    return {"image": base64.b64encode(data).decode(), "format": "jpeg", "size": len(data)}
