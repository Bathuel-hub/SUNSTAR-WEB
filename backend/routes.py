from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import logging

from database import get_database
from models import (
    CompanyInfo, ProductCategory, Product, ContactInquiry, ContactInquiryCreate,
    Testimonial, Advantage, SuccessResponse, ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Company Information Endpoints
@router.get("/company-info", response_model=CompanyInfo)
async def get_company_info():
    """Get company information"""
    try:
        db = get_database()
        company_data = await db.company_info.find_one({}, {"_id": 0})
        
        if not company_data:
            raise HTTPException(status_code=404, detail="Company information not found")
        
        return CompanyInfo(**company_data)
    except Exception as e:
        logger.error(f"Error fetching company info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Product Endpoints
@router.get("/products/categories", response_model=List[ProductCategory])
async def get_product_categories():
    """Get all product categories"""
    try:
        db = get_database()
        categories = []
        
        async for category in db.product_categories.find({}, {"_id": 0}):
            categories.append(ProductCategory(**category))
        
        return categories
    except Exception as e:
        logger.error(f"Error fetching product categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/products/category/{category_id}", response_model=List[Product])
async def get_products_by_category(category_id: str):
    """Get products by category ID"""
    try:
        db = get_database()
        products = []
        
        async for product in db.products.find({"category_id": category_id}, {"_id": 0}):
            products.append(Product(**product))
        
        return products
    except Exception as e:
        logger.error(f"Error fetching products for category {category_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/products/sample/{category_id}")
async def get_sample_products(category_id: str):
    """Get sample products for display"""
    sample_products = {
        "1": [
            {"name": "Toyota Camry 2024", "specs": "2.5L Engine, CVT, LED Headlights", "price": "Contact for Price"},
            {"name": "Honda Accord 2024", "specs": "1.5L Turbo, Hybrid Available", "price": "Contact for Price"},
            {"name": "Nissan Altima 2024", "specs": "2.0L VC-Turbo, ProPILOT Assist", "price": "Contact for Price"},
            {"name": "Hyundai Sonata 2024", "specs": "2.5L GDI, SmartSense Safety", "price": "Contact for Price"}
        ],
        "2": [
            {"name": "Engine Oil Filters", "specs": "Compatible with major brands", "price": "From $15"},
            {"name": "Brake Pads Set", "specs": "Ceramic & Semi-Metallic options", "price": "From $45"},
            {"name": "Transmission Parts", "specs": "OEM & Aftermarket quality", "price": "Contact for Price"},
            {"name": "Air Intake Systems", "specs": "Performance & Standard grades", "price": "From $120"}
        ],
        "3": [
            {"name": "Hydraulic Cylinders", "specs": "Various bore sizes available", "price": "Contact for Price"},
            {"name": "Track Chains", "specs": "Heavy-duty steel construction", "price": "Contact for Price"},
            {"name": "Engine Overhaul Kits", "specs": "Complete rebuild packages", "price": "Contact for Price"},
            {"name": "Hydraulic Pumps", "specs": "OEM replacements available", "price": "Contact for Price"}
        ],
        "4": [
            {"name": "Excavator CAT 320", "specs": "20-ton operating weight", "price": "Contact for Price"},
            {"name": "Bulldozer D6T", "specs": "Track-type tractor", "price": "Contact for Price"},
            {"name": "Mobile Crane 50T", "specs": "Hydraulic telescopic boom", "price": "Contact for Price"},
            {"name": "Concrete Mixer Truck", "specs": "8-12 cubic meter capacity", "price": "Contact for Price"}
        ]
    }
    
    return sample_products.get(category_id, [])

# Contact & Inquiry Endpoints
@router.post("/contact/inquiry", response_model=SuccessResponse)
async def create_contact_inquiry(
    inquiry: ContactInquiryCreate,
    request: Request,
    background_tasks: BackgroundTasks
):
    """Submit a contact inquiry"""
    try:
        db = get_database()
        
        # Get client IP and user agent
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Create inquiry document
        inquiry_data = inquiry.dict()
        inquiry_data.update({
            "status": "new",
            "ip_address": client_ip,
            "user_agent": user_agent,
            "created_at": datetime.utcnow()
        })
        
        inquiry_obj = ContactInquiry(**inquiry_data)
        inquiry_dict = inquiry_obj.dict()
        
        # Save to database
        result = await db.inquiries.insert_one(inquiry_dict)
        
        # Schedule background email notification (placeholder for now)
        background_tasks.add_task(send_inquiry_notification, inquiry_obj)
        
        return SuccessResponse(
            message="Thank you for your inquiry! We will contact you within 24 hours.",
            data={"inquiry_id": inquiry_obj.id}
        )
    except Exception as e:
        logger.error(f"Error creating contact inquiry: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit inquiry")

@router.get("/contact/inquiries", response_model=List[ContactInquiry])
async def get_contact_inquiries(status: Optional[str] = None, limit: int = 50):
    """Get contact inquiries (admin endpoint)"""
    try:
        db = get_database()
        
        filter_query = {}
        if status:
            filter_query["status"] = status
        
        inquiries = []
        async for inquiry in db.inquiries.find(filter_query, {"_id": 0}).limit(limit):
            inquiries.append(ContactInquiry(**inquiry))
        
        return inquiries
    except Exception as e:
        logger.error(f"Error fetching inquiries: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Testimonials Endpoints
@router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(featured_only: bool = True):
    """Get testimonials"""
    try:
        db = get_database()
        
        filter_query = {"is_active": True}
        if featured_only:
            filter_query["is_featured"] = True
        
        testimonials = []
        async for testimonial in db.testimonials.find(filter_query, {"_id": 0}):
            testimonials.append(Testimonial(**testimonial))
        
        return testimonials
    except Exception as e:
        logger.error(f"Error fetching testimonials: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Why Choose Us Endpoints
@router.get("/advantages", response_model=List[Advantage])
async def get_advantages():
    """Get competitive advantages"""
    try:
        db = get_database()
        
        advantages = []
        async for advantage in db.advantages.find(
            {"is_active": True}, 
            {"_id": 0}
        ).sort("order", 1):
            advantages.append(Advantage(**advantage))
        
        return advantages
    except Exception as e:
        logger.error(f"Error fetching advantages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Statistics Endpoint
@router.get("/stats")
async def get_stats():
    """Get website statistics"""
    try:
        db = get_database()
        
        stats = {
            "total_inquiries": await db.inquiries.count_documents({}),
            "new_inquiries": await db.inquiries.count_documents({"status": "new"}),
            "total_testimonials": await db.testimonials.count_documents({"is_active": True}),
            "product_categories": await db.product_categories.count_documents({})
        }
        
        return stats
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Background Tasks
async def send_inquiry_notification(inquiry: ContactInquiry):
    """Send email notification for new inquiry (placeholder)"""
    # This is a placeholder for email notification functionality
    # In a real implementation, you would integrate with an email service
    logger.info(f"New inquiry received from {inquiry.name} ({inquiry.email})")
    logger.info(f"Inquiry type: {inquiry.inquiry_type}")
    logger.info(f"Message: {inquiry.message}")