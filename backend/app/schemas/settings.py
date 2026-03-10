from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class HeroSettings(BaseModel):
    bannerImg: str
    title: str
    subtitle: str
    btnText: str
    btnLink: str

class CouponSettings(BaseModel):
    label: str
    discount: str
    text: str
    code: str

class HighlightItem(BaseModel):
    id: int
    title: str
    image: str
    subtitle: str
    link: str

class HomeCategoryItem(BaseModel):
    id: int
    name: str
    image: str
    path: str

class FooterSettings(BaseModel):
    storeName: str
    description: str
    newsletterText: str
    copyright: str
    credit: str
    instagram: str

class NavCategoryItem(BaseModel):
    name: str
    path: str
    dropdown: List[str]

class SiteSettings(BaseModel):
    hero: Optional[HeroSettings] = None
    coupon: Optional[CouponSettings] = None
    highlights: Optional[List[HighlightItem]] = None
    homeCategories: Optional[List[HomeCategoryItem]] = None
    footer: Optional[FooterSettings] = None
    navCategories: Optional[List[NavCategoryItem]] = None
    heroSliders: Optional[List[Dict[str, Any]]] = None
    # sectionCategories and products are usually dynamic or from other models
    # but we can include them if the CMS manages them directly
    sectionCategories: Optional[Dict[str, List[Dict[str, Any]]]] = None

class SettingsResponse(BaseModel):
    config: Dict[str, Any]
