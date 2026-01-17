from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole

#---Pydantic Model (Schema)---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    
    model_config = {
         "from_attributes": True 
    }

    

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str]
    price: float

class ProductShort(ProductCreate):
    model_config = {
         "from_attributes": True 
    }
    
class InventoryCreate(BaseModel):
    product_id: int
    available_qty: int
    
    
class InventoryUpdate(BaseModel):
    available_qty: int
    
class InvetoryShort(BaseModel):
    available_qty: int
    updated_at: datetime
    
    model_config = {
         "from_attributes": True 
    }
    
class InventoryResponse(BaseModel):
    product_id: int
    available_qty: int
    updated_at: datetime
    product: ProductShort
    
    model_config = {
         "from_attributes": True 
    }
    
class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    inventory: InvetoryShort | None
    is_active: bool
    created_at: datetime
    
    model_config = {
         "from_attributes": True 
    }
    


class OrderItemCreate(BaseModel):
    product_id: int
    qty: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    
    
class OrderItemResponse(BaseModel):
    product_id: int
    qty: int
    unit_price: float
    
    model_config = {
         "from_attributes": True 
    }
    
class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]
    
    model_config = {
         "from_attributes": True 
    }
    
class Login(BaseModel):
    username: str
    password: str
    
class TokenData(BaseModel):
    # email: str | None = None
    email: str