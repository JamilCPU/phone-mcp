from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.shell import run_command

router = APIRouter(prefix="/input", tags=["input"], dependencies=[Depends(verify_token)])


class TapRequest(BaseModel):
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)


@router.post("/tap")
async def tap(req: TapRequest):
    result = await run_command(f"input tap {req.x} {req.y}", timeout=5)
    return {"tapped": True, "x": req.x, "y": req.y, "stdout": result.stdout}


class SwipeRequest(BaseModel):
    x1: int = Field(..., ge=0)
    y1: int = Field(..., ge=0)
    x2: int = Field(..., ge=0)
    y2: int = Field(..., ge=0)
    duration_ms: int = Field(default=300, ge=50, le=5000)


@router.post("/swipe")
async def swipe(req: SwipeRequest):
    result = await run_command(
        f"input swipe {req.x1} {req.y1} {req.x2} {req.y2} {req.duration_ms}", timeout=10
    )
    return {"swiped": True, "result": result.stdout}


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


@router.post("/text")
async def type_text(req: TextRequest):
    safe = req.text.replace(" ", "%s").replace("'", "\'").replace('"', '\\"')
    result = await run_command(f'input text "{safe}"', timeout=10)
    return {"typed": True, "result": result.stdout}


class KeyRequest(BaseModel):
    keycode: str = Field(..., description="Android keycode, e.g. KEYCODE_BACK, KEYCODE_HOME")


@router.post("/key")
async def press_key(req: KeyRequest):
    result = await run_command(f"input keyevent {req.keycode}", timeout=5)
    return {"key_pressed": req.keycode, "result": result.stdout}
