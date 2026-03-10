from fastapi import APIRouter, HTTPException, Request, Body, status, Depends
from app.routes.auth import get_current_admin_user
from typing import Dict, Any

router = APIRouter()

@router.get("/")
async def get_settings(request: Request):
    settings = await request.app.mongodb["settings"].find_one({"id": "site_config"})
    if not settings:
        # If no settings found, return an empty config or we can set initial defaults
        return {"config": {}}
    
    # Remove MongoDB internal ID for clean response
    settings.pop("_id", None)
    return {"config": settings.get("config", {})}

@router.post("/")
async def update_settings(
    request: Request, 
    data: Dict[str, Any] = Body(...),
    admin_user: dict = Depends(get_current_admin_user)
):
    # Upsert the settings document
    result = await request.app.mongodb["settings"].update_one(
        {"id": "site_config"},
        {"$set": {"config": data, "updated_at": "now"}}, # Simple timestamp or OMIT
        upsert=True
    )
    
    if result.modified_count or result.upserted_id:
        return {"message": "Settings updated successfully"}
    
    # Even if nothing changed, if the update call was successful, return OK
    return {"message": "Settings already up to date"}
