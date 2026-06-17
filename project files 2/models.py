from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    price: float
    category: str
    image_url: str
    rating: float = 0.0
    stock: int = 100
    tags: List[str] = []

class UserInteraction(BaseModel):
    user_id: str
    product_id: str
    action: str  # 'view', 'add_to_cart', 'purchase'
    timestamp: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: str
    preferences: List[str] = []

class RecommendationResponse(BaseModel):
    user_id: str
    recommended_products: List[Product]
