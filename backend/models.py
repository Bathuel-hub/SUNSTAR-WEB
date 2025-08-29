from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Company Information Models
class CompanyInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    license_no: str
    manager: str
    tagline: str
    mission: str
    values: List[str]
    address: Dict[str, str]
    contact: Dict[str, str]
    license: Dict[str, str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Product Models
class ProductCategory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    image: str
    products: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category_id: str
    name: str
    description: str
    specifications: str
    price: str
    image: Optional[str] = None
    availability: str = "Available"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Contact & Inquiry Models
class ContactInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    inquiry_type: str
    message: str
    status: str = "new"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ContactInquiryCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    inquiry_type: str
    message: str

# Testimonial Models
class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: str
    text: str
    rating: int = Field(ge=1, le=5)
    is_featured: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TestimonialCreate(BaseModel):
    name: str
    company: str
    text: str
    rating: int = Field(ge=1, le=5)

# Why Choose Us Models
class Advantage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    icon: str
    order: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None