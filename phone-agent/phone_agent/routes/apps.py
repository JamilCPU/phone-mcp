from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..utils.shell import run_command

router = APIRouter(prefix="/apps", tags=["apps"], dependencies=[Depends(verify_token)])


@router.get("")
async def list_apps():
    result = await run_command("pm list packages -3", timeout=20)
    packages = [
        line.removeprefix("package:").strip()
        for line in result.stdout.splitlines()
        if line.startswith("package:")
    ]
    return {"packages": packages, "count": len(packages)}


class AppLaunchRequest(BaseModel):
    package: str = Field(..., min_length=1)
    activity: str = ""


@router.post("/launch")
async def launch_app(req: AppLaunchRequest):
    cmd = (f"am start -n {req.package}/{req.activity}" if req.activity
           else f"monkey -p {req.package} -c android.intent.category.LAUNCHER 1")
    result = await run_command(cmd, timeout=10)
    if result.exit_code != 0:
        raise HTTPException(status_code=500, detail=f"Failed to launch: {result.stderr}")
    return {"launched": req.package, "stdout": result.stdout}
