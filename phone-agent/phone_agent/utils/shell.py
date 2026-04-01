import asyncio
import os
import signal
from typing import NamedTuple


class ShellResult(NamedTuple):
    stdout: str
    stderr: str
    exit_code: int


async def run_command(command: str, timeout: int = 30) -> ShellResult:
    if not command or not command.strip():
        return ShellResult(stdout="", stderr="Command cannot be empty", exit_code=1)

    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        preexec_fn=os.setsid,
    )
    try:
        stdout_b, stderr_b = await asyncio.wait_for(
            proc.communicate(), timeout=float(timeout)
        )
        return ShellResult(
            stdout=stdout_b.decode("utf-8", errors="replace"),
            stderr=stderr_b.decode("utf-8", errors="replace"),
            exit_code=proc.returncode or 0,
        )
    except asyncio.TimeoutError:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        return ShellResult(stdout="", stderr=f"Command timed out after {timeout}s", exit_code=124)
