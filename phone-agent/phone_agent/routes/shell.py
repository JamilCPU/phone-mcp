from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..config import settings
from ..utils.shell import run_command

router = APIRouter(prefix="/shell", tags=["shell"], dependencies=[Depends(verify_token)])


class ShellRequest(BaseModel):
    command: str = Field(..., min_length=1)
    timeout: int = Field(default=30, ge=1, le=300)


class ShellResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    blocked: bool = False


@router.post("", response_model=ShellResponse)
async def execute_shell(req: ShellRequest) -> ShellResponse:
    for blocked in settings.blocked_command_list:
        if blocked and blocked in req.command:
            return ShellResponse(stdout="", stderr=f"Command blocked: contains '{blocked}'", exit_code=1, blocked=True)
    timeout = min(req.timeout, settings.max_shell_timeout)
    result = await run_command(req.command, timeout=timeout)
    return ShellResponse(stdout=result.stdout, stderr=result.stderr, exit_code=result.exit_code)
