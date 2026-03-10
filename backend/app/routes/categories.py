from fastapi import APIRouter, HTTPException, Request, Body, status
from fastapi.responses import JSONResponse
from app.schemas.categories import CategoryCreate, CategoryUpdate
from typing import List, Optional
from bson import ObjectId

router = APIRouter()

@router.get("/", response_description="List all categories")
async def list_categories(request: Request):
    categories = []
    cursor = request.app.mongodb["categories"].find()
    async for category in cursor:
        category["_id"] = str(category["_id"])
        categories.append(category)
    return categories

@router.get("/{id}", response_description="Get a single category")
async def show_category(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    if (category := await request.app.mongodb["categories"].find_one({"_id": ObjectId(id)})) is not None:
        category["_id"] = str(category["_id"])
        return category
    
    raise HTTPException(status_code=404, detail=f"Category {id} not found")

@router.post("/", response_description="Add new category", status_code=status.HTTP_201_CREATED)
async def create_category(request: Request, category: CategoryCreate = Body(...)):
    category_dict = category.dict()
    new_category = await request.app.mongodb["categories"].insert_one(category_dict)
    created_category = await request.app.mongodb["categories"].find_one({"_id": new_category.inserted_id})
    created_category["_id"] = str(created_category["_id"])
    return created_category

@router.delete("/{id}", response_description="Delete a category")
async def delete_category(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    delete_result = await request.app.mongodb["categories"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Category {id} not found")
