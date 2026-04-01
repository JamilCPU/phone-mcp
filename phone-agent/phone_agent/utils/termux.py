"""Async wrappers around termux-* commands."""
import json
from .shell import run_command, ShellResult


async def termux_cmd(cmd: str, timeout: int = 15) -> dict | list | str:
    result = await run_command(cmd, timeout=timeout)
    if result.exit_code != 0:
        return {"error": result.stderr or f"Command failed: {cmd}"}
    output = result.stdout.strip()
    if not output:
        return {}
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return output


async def battery_status() -> dict:
    return await termux_cmd("termux-battery-status")


async def send_notification(title: str, content: str, id: int = 1) -> dict:
    safe_title = title.replace('"', '\\"')
    safe_content = content.replace('"', '\\"')
    return await termux_cmd(
        f'termux-notification --id {id} --title "{safe_title}" --content "{safe_content}"'
    )


async def clipboard_get() -> str:
    result = await termux_cmd("termux-clipboard-get")
    return str(result)


async def clipboard_set(text: str) -> dict:
    safe = text.replace("'", "'\''")
    return await termux_cmd(f"termux-clipboard-set '{safe}'")


async def sms_list(limit: int = 10) -> list:
    result = await termux_cmd(f"termux-sms-list -l {limit}", timeout=20)
    return result if isinstance(result, list) else []


async def sms_send(number: str, body: str) -> dict:
    safe_body = body.replace('"', '\\"')
    return await termux_cmd(f'termux-sms-send -n "{number}" "{safe_body}"', timeout=30)


async def contact_list() -> list:
    result = await termux_cmd("termux-contact-list", timeout=20)
    return result if isinstance(result, list) else []


async def get_location(provider: str = "gps") -> dict:
    return await termux_cmd(f"termux-location -p {provider} -r once", timeout=30)


async def set_volume(stream: str, value: int) -> dict:
    return await termux_cmd(f"termux-volume {stream} {value}")


async def get_volume() -> dict:
    return await termux_cmd("termux-volume")


async def torch(on: bool) -> dict:
    state = "on" if on else "off"
    return await termux_cmd(f"termux-torch {state}")


async def vibrate(duration_ms: int = 500) -> dict:
    return await termux_cmd(f"termux-vibrate -d {duration_ms} -f")


async def tts_speak(text: str, language: str = "en") -> dict:
    safe = text.replace('"', '\\"')
    return await termux_cmd(f'termux-tts-speak -l {language} "{safe}"', timeout=30)


async def camera_photo(camera_id: int = 0) -> bytes | None:
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        path = f.name
    try:
        result = await run_command(f"termux-camera-photo -c {camera_id} {path}", timeout=15)
        if result.exit_code == 0 and os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return None
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


async def wifi_info() -> dict:
    return await termux_cmd("termux-wifi-connectioninfo")
