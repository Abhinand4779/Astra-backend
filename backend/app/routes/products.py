from fastapi import APIRouter, HTTPException, Request, Body, status
from fastapi.responses import JSONResponse
from app.schemas.products import ProductCreate, ProductUpdate
from typing import List, Optional
from bson import ObjectId

router = APIRouter()

@router.get("/", response_description="List all products")
async def list_products(
    request: Request, 
    category: Optional[str] = None, 
    section: Optional[str] = None,
    has_discount: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "created_at",
    order: Optional[int] = -1 # -1 for desc, 1 for asc
):
    query = {}
    if category:
        query["category"] = category
    if section:
        query["section"] = section
    if has_discount:
        query["discount"] = {"$exists": True, "$ne": None}
    
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    
    products = []
    # Cursor to list
    cursor = request.app.mongodb["products"].find(query).sort(sort_by, order)
    async for product in cursor:
        product["_id"] = str(product["_id"])
        products.append(product)
    
    return products

@router.get("/{id}", response_description="Get a single product")
async def show_product(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    if (product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id)})) is not None:
        product["_id"] = str(product["_id"])
        return product
    
    raise HTTPException(status_code=404, detail=f"Product {id} not found")

@router.post("/", response_description="Add new product", status_code=status.HTTP_201_CREATED)
async def create_product(request: Request, product: ProductCreate = Body(...)):
    product_dict = product.dict()
    new_product = await request.app.mongodb["products"].insert_one(product_dict)
    created_product = await request.app.mongodb["products"].find_one({"_id": new_product.inserted_id})
    created_product["_id"] = str(created_product["_id"])
    return created_product

@router.put("/{id}", response_description="Update a product")
async def update_product(request: Request, id: str, product: ProductUpdate = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    product_dict = {k: v for k, v in product.dict().items() if v is not None}
    
    if len(product_dict) >= 1:
        update_result = await request.app.mongodb["products"].update_one(
            {"_id": ObjectId(id)}, {"$set": product_dict}
        )

        if update_result.modified_count == 1:
            if (
                updated_product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id)})
            ) is not None:
                updated_product["_id"] = str(updated_product["_id"])
                return updated_product

    if (
        existing_product := await request.app.mongodb["products"].find_one({"_id": ObjectId(id)})
    ) is not None:
        existing_product["_id"] = str(existing_product["_id"])
        return existing_product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")

@router.delete("/{id}", response_description="Delete a product")
async def delete_product(request: Request, id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    delete_result = await request.app.mongodb["products"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")
