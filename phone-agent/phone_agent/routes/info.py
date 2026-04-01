import platform
import asyncio
from fastapi import APIRouter, Depends
from ..auth import verify_token
from ..utils.termux import battery_status, wifi_info
from ..utils.shell import run_command

router = APIRouter(prefix="/info", tags=["info"], dependencies=[Depends(verify_token)])


@router.get("")
async def device_info():
    results = await asyncio.gather(
        battery_status(), wifi_info(),
        run_command("df -h /sdcard 2>/dev/null || df -h /data"),
        run_command("uname -a"),
        return_exceptions=True,
    )
    battery, wifi, disk_r, uname_r = results
    return {
        "platform": platform.platform(),
        "battery": battery if not isinstance(battery, Exception) else {},
        "wifi": wifi if not isinstance(wifi, Exception) else {},
        "disk": disk_r.stdout if not isinstance(disk_r, Exception) else "",
        "uname": uname_r.stdout.strip() if not isinstance(uname_r, Exception) else "",
    }
