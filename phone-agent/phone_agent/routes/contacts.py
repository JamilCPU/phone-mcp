from fastapi import APIRouter, Depends
from ..auth import verify_token
from ..utils.termux import contact_list

router = APIRouter(prefix="/contacts", tags=["contacts"], dependencies=[Depends(verify_token)])


@router.get("")
async def list_contacts():
    contacts = await contact_list()
    return {"contacts": contacts, "count": len(contacts)}
