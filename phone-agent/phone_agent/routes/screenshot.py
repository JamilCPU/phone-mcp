import base64
import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException
from ..auth import verify_token
from ..utils.shell import run_command

router = APIRouter(prefix="/screenshot", tags=["screenshot"], dependencies=[Depends(verify_token)])


@router.get("")
async def take_screenshot():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = f.name
    try:
        result = await run_command(f"termux-screenshot -f {path}", timeout=15)
        if result.exit_code != 0 or not os.path.exists(path) or os.path.getsize(path) == 0:
            result = await run_command(f"screencap -p {path}", timeout=15)
        if result.exit_code != 0 or not os.path.exists(path) or os.path.getsize(path) == 0:
            raise HTTPException(status_code=503, detail=f"Screenshot failed: {result.stderr}")
        data = open(path, "rb").read()
        return {"image": base64.b64encode(data).decode(), "format": "png", "size": len(data)}
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
