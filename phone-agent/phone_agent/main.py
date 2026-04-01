import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .config import settings
from .routes import (
    shell, files, info, screenshot, notification, clipboard,
    sms, contacts, location, media, volume, apps,
)
from .routes import input as input_router

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("phone-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.phone_agent_key:
        logger.warning("PHONE_AGENT_KEY not set — running without authentication!")
    else:
        logger.info("Authentication enabled")
    logger.info(f"Phone agent ready on port {settings.phone_agent_port}")
    yield


app = FastAPI(
    title="Phone MCP Agent",
    description="HTTP agent exposing Android phone capabilities for AI model control",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


for router in [
    shell.router, files.router, info.router, screenshot.router,
    notification.router, clipboard.router, sms.router, contacts.router,
    location.router, media.router, volume.router, apps.router,
    input_router.router,
]:
    app.include_router(router)


def run():
    import uvicorn
    uvicorn.run(
        "phone_agent.main:app",
        host=settings.phone_agent_host,
        port=settings.phone_agent_port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run()
