import base64
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from ..auth import verify_token
from ..config import settings

router = APIRouter(prefix="/files", tags=["files"], dependencies=[Depends(verify_token)])
MAX_BYTES = settings.max_file_size_mb * 1024 * 1024


def _safe_path(path: str) -> Path:
    if not os.path.isabs(path):
        raise HTTPException(status_code=400, detail="Path must be absolute")
    return Path(path)


@router.get("")
async def read_file(path: str = Query(...)):
    p = _safe_path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    if not p.is_file():
        raise HTTPException(status_code=400, detail="Path is not a file")
    size = p.stat().st_size
    if size > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"File too large: {size} bytes")
    raw = p.read_bytes()
    try:
        return {"path": path, "content": raw.decode("utf-8"), "encoding": "utf-8", "size": size}
    except UnicodeDecodeError:
        return {"path": path, "content": base64.b64encode(raw).decode(), "encoding": "base64", "size": size}


class WriteRequest(BaseModel):
    path: str
    content: str
    encoding: str = "utf-8"


@router.post("")
async def write_file(req: WriteRequest):
    p = _safe_path(req.path)
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(req.content) if req.encoding == "base64" else req.content.encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Content too large")
    p.write_bytes(raw)
    return {"path": req.path, "written": len(raw)}


@router.get("/list")
async def list_directory(path: str = Query(default="/sdcard")):
    p = _safe_path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {path}")
    if not p.is_dir():
        raise HTTPException(status_code=400, detail="Path is not a directory")
    entries = []
    for entry in sorted(p.iterdir(), key=lambda e: (e.is_file(), e.name)):
        stat = entry.stat()
        entries.append({
            "name": entry.name,
            "path": str(entry),
            "is_directory": entry.is_dir(),
            "size": stat.st_size if entry.is_file() else None,
            "modified": stat.st_mtime,
        })
    return {"path": path, "entries": entries}
