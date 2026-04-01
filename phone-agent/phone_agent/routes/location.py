from fastapi import APIRouter, Depends, Query
from ..auth import verify_token
from ..utils.termux import get_location

router = APIRouter(prefix="/location", tags=["location"], dependencies=[Depends(verify_token)])


@router.get("")
async def location(provider: str = Query(default="gps", enum=["gps", "network", "passive"])):
    return await get_location(provider)
