from pydantic import BaseModel, Field
from typing import List, Optional

class CategorySchema(BaseModel):
    name: str = Field(...)
    slug: str = Field(...)
    description: Optional[str] = None
    subcategories: List[str] = Field(default=[])

class CategoryCreate(CategorySchema):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    subcategories: Optional[List[str]] = None
