from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
from datetime import datetime
import logging
import os
import uuid
import shutil
from pathlib import Path

from database import get_database
from models import (
    CompanyInfo, ProductCategory, Product, ContactInquiry, ContactInquiryCreate,
    Testimonial, Advantage, SuccessResponse, ErrorResponse, CustomerRating, 
    CustomerRatingCreate, ProductItem, ProductItemCreate
)
from email_service import email_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

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

# Customer Rating Endpoints
@router.post("/ratings", response_model=SuccessResponse)
async def create_customer_rating(
    rating: CustomerRatingCreate,
    request: Request
):
    """Submit a customer rating/review"""
    try:
        db = get_database()
        
        # Get client IP
        client_ip = request.client.host
        
        # Create rating document
        rating_data = rating.dict()
        rating_data.update({
            "ip_address": client_ip,
            "created_at": datetime.utcnow()
        })
        
        rating_obj = CustomerRating(**rating_data)
        rating_dict = rating_obj.dict()
        
        # Save to database
        await db.customer_ratings.insert_one(rating_dict)
        
        return SuccessResponse(
            message="Thank you for your feedback! Your rating has been recorded.",
            data={"rating_id": rating_obj.id}
        )
    except Exception as e:
        logger.error(f"Error creating customer rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit rating")

@router.get("/ratings", response_model=List[CustomerRating])
async def get_customer_ratings(limit: int = 10, category: Optional[str] = None):
    """Get customer ratings (public endpoint)"""
    try:
        db = get_database()
        
        filter_query = {}
        if category:
            filter_query["service_category"] = category
        
        ratings = []
        async for rating in db.customer_ratings.find(
            filter_query, 
            {"_id": 0}
        ).sort("created_at", -1).limit(limit):
            ratings.append(CustomerRating(**rating))
        
        return ratings
    except Exception as e:
        logger.error(f"Error fetching ratings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Product Management Endpoints
@router.get("/admin/products", response_model=List[ProductItem])
async def get_admin_products():
    """Get all products for admin management"""
    try:
        db = get_database()
        
        products = []
        async for product in db.admin_products.find({}, {"_id": 0}):
            products.append(ProductItem(**product))
        
        return products
    except Exception as e:
        logger.error(f"Error fetching admin products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/admin/products", response_model=SuccessResponse)
async def create_admin_product(product: ProductItemCreate):
    """Create a new product (admin only)"""
    try:
        db = get_database()
        
        product_obj = ProductItem(**product.dict())
        product_dict = product_obj.dict()
        
        await db.admin_products.insert_one(product_dict)
        
        return SuccessResponse(
            message="Product created successfully",
            data={"product_id": product_obj.id}
        )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.delete("/admin/products/{product_id}", response_model=SuccessResponse)
async def delete_admin_product(product_id: str):
    """Delete a product (admin only)"""
    try:
        db = get_database()
        
        result = await db.admin_products.delete_one({"id": product_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return SuccessResponse(message="Product deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete product")

@router.put("/admin/products/{product_id}", response_model=SuccessResponse)
async def update_admin_product(product_id: str, product: ProductItemCreate):
    """Update a product (admin only)"""
    try:
        db = get_database()
        
        update_data = product.dict()
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.admin_products.update_one(
            {"id": product_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return SuccessResponse(message="Product updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")

# File Upload Endpoints
@router.post("/upload/images", response_model=SuccessResponse)
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """Upload multiple image files for products"""
    try:
        if len(files) > 10:  # Limit to 10 images per upload
            raise HTTPException(status_code=400, detail="Maximum 10 images allowed per upload")
        
        uploaded_files = []
        errors = []
        
        for file in files:
            try:
                # Validate file type
                if not file.content_type.startswith('image/'):
                    errors.append(f"{file.filename}: Must be an image file")
                    continue
                
                # Read and validate file size
                content = await file.read()
                file_size = len(content)
                
                if file_size > 5 * 1024 * 1024:  # 5MB
                    errors.append(f"{file.filename}: File size must be less than 5MB")
                    continue
                
                # Generate unique filename
                file_extension = os.path.splitext(file.filename)[1].lower()
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = UPLOAD_DIR / unique_filename
                
                # Save file
                with open(file_path, "wb") as buffer:
                    buffer.write(content)
                
                # Add to successful uploads
                file_url = f"/api/uploads/{unique_filename}"
                uploaded_files.append({
                    "file_url": file_url,
                    "filename": unique_filename,
                    "original_name": file.filename,
                    "size": file_size
                })
                
                # Reset file position for next file
                await file.seek(0)
                
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
                continue
        
        if not uploaded_files and errors:
            raise HTTPException(status_code=400, detail=f"No files uploaded successfully. Errors: {'; '.join(errors)}")
        
        logger.info(f"Bulk upload completed: {len(uploaded_files)} successful, {len(errors)} errors")
        
        response_data = {
            "uploaded_files": uploaded_files,
            "upload_count": len(uploaded_files),
            "total_files": len(files)
        }
        
        if errors:
            response_data["errors"] = errors
        
        return SuccessResponse(
            message=f"Successfully uploaded {len(uploaded_files)} out of {len(files)} images",
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload images")

@router.delete("/upload/image/{filename}", response_model=SuccessResponse)
async def delete_image(filename: str):
    """Delete an uploaded image file"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if file_path.exists():
            os.remove(file_path)
            return SuccessResponse(message="Image deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete image")

@router.get("/uploads/{filename}")
async def serve_uploaded_file(filename: str):
    """Serve uploaded image files"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Security check: ensure filename doesn't contain path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        return FileResponse(
            path=file_path,
            media_type="image/jpeg",  # Will be overridden by FastAPI based on file extension
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        raise HTTPException(status_code=500, detail="Failed to serve file")

# Background Tasks
async def send_inquiry_notification(inquiry: ContactInquiry):
    """Send email notification for new inquiry using email service"""
    try:
        success = await email_service.send_contact_email(inquiry)
        if success:
            logger.info(f"✅ Email notification sent for inquiry {inquiry.id}")
        else:
            logger.error(f"❌ Failed to send email notification for inquiry {inquiry.id}")
    except Exception as e:
        logger.error(f"❌ Error sending inquiry notification: {e}")

# Email Functions (Remove the old placeholder function)
# The old send_contact_email function is replaced by email_service.send_contact_email