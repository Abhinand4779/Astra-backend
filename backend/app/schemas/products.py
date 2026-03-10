from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductSchema(BaseModel):
    name: str = Field(...)
    price: float = Field(...)  # Store as number for better sorting/filtering
    price_display: str = Field(...) # e.g. "₹85,000"
    oldPrice: Optional[float] = None
    oldPrice_display: Optional[str] = None
    discount: Optional[str] = None
    category: str = Field(...)
    section: str = Field(...) # Women, Men, Kids
    description: str = Field(...)
    details: List[str] = Field(default=[])
    images: List[str] = Field(default=[])
    material: Optional[str] = None
    size: Optional[List[str]] = None
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductResponse(ProductSchema):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {
            # Handle ObjectId if needed
        }

class ProductCreate(ProductSchema):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    price_display: Optional[str] = None
    oldPrice: Optional[float] = None
    oldPrice_display: Optional[str] = None
    discount: Optional[str] = None
    category: Optional[str] = None
    section: Optional[str] = None
    description: Optional[str] = None
    details: Optional[List[str]] = None
    images: Optional[List[str]] = None
    material: Optional[str] = None
    size: Optional[List[str]] = None
    is_featured: Optional[bool] = None
