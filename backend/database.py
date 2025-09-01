from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None

def get_database() -> AsyncIOMotorClient:
    return Database.db

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'sunstar_db')
    
    try:
        Database.client = AsyncIOMotorClient(mongo_url)
        Database.db = Database.client[db_name]
        
        # Test the connection
        await Database.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Initialize collections and sample data
        await initialize_database()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if Database.client:
        Database.client.close()
        logger.info("MongoDB connection closed")

async def initialize_database():
    """Initialize database with sample data if collections are empty"""
    db = get_database()
    
    # Company Information
    company_collection = db.company_info
    # Always update to ensure latest contact info
    await company_collection.delete_many({})  # Clear existing data
        company_data = {
            "name": "SUN STAR INTERNATIONAL FZ-LLC",
            "license_no": "5034384",
            "manager": "Daniel Abera Wakjira",
            "tagline": "Driving Growth. Powering Construction.",
            "mission": "To connect global markets with high-quality cars, spare parts, and heavy equipment.",
            "values": ["Trust", "Reliability", "Speed"],
            "address": {
                "building": "VVIPR1315, Compass building - Al Hulaila",
                "zone": "AL Hulaila Industrial Zone-FZ",
                "city": "RAK UAE",
                "country": "United Arab Emirates"
            },
            "contact": {
                "phoneUAE": "+971551849702",
                "phoneEthiopia": "+251-911373857",
                "email": "sunstarintl.ae@gmail.com",
                "whatsapp": "+971551849702"
            },
            "license": {
                "issueDate": "11-08-2025",
                "expiryDate": "10-08-2026",
                "authority": "RAKEZ"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await company_collection.insert_one(company_data)
        logger.info("Company information initialized")

    # Product Categories
    categories_collection = db.product_categories
    if await categories_collection.count_documents({}) == 0:
        categories_data = [
            {
                "name": "New Passenger Motor Vehicles",
                "description": "High-quality new passenger cars from trusted global manufacturers",
                "image": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7",
                "products": ["Sedans", "SUVs", "Hatchbacks", "Luxury Vehicles"],
                "created_at": datetime.utcnow()
            },
            {
                "name": "Auto Spare Parts & Components",
                "description": "Comprehensive range of automotive parts and components",
                "image": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxhdXRvbW90aXZlJTIwcGFydHN8ZW58MHx8fHwxNzU2NDk3Nzg5fDA&ixlib=rb-4.1.0&q=85",
                "products": ["Engines", "Transmissions", "Body Parts", "Electrical Components"],
                "created_at": datetime.utcnow()
            },
            {
                "name": "Heavy Equipment & Machinery Spare Parts",
                "description": "Durable spare parts for heavy machinery and construction equipment",
                "image": "https://images.unsplash.com/photo-1635691033744-a1a2a07ba971?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwxfHxlbmdpbmVzfGVufDB8fHx8MTc1NjQ5Nzc5N3ww&ixlib=rb-4.1.0&q=85",
                "products": ["Hydraulic Parts", "Engine Components", "Tracks & Tires", "Filters & Fluids"],
                "created_at": datetime.utcnow()
            },
            {
                "name": "Construction Equipment & Machinery",
                "description": "Professional construction machinery for all your project needs",
                "image": "https://images.unsplash.com/photo-1717386255773-1e3037c81788?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxtYWNoaW5lcnl8ZW58MHx8fHwxNzU2NDk3ODA0fDA&ixlib=rb-4.1.0&q=85",
                "products": ["Excavators", "Bulldozers", "Cranes", "Loaders", "Concrete Mixers"],
                "created_at": datetime.utcnow()
            }
        ]
        await categories_collection.insert_many(categories_data)
        logger.info("Product categories initialized")

    # Testimonials
    testimonials_collection = db.testimonials
    if await testimonials_collection.count_documents({}) == 0:
        testimonials_data = [
            {
                "name": "Ahmed Al-Rashid",
                "company": "Al-Rashid Construction",
                "text": "Sun Star International provided us with excellent construction equipment. Their professionalism and quick delivery exceeded our expectations.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Mohammed Hassan",
                "company": "Hassan Auto Trading",
                "text": "The quality of spare parts and competitive pricing makes Sun Star our preferred supplier for automotive components.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Sarah Williams",
                "company": "International Logistics Ltd",
                "text": "Reliable partner for our equipment needs across the Middle East. Professional service and quality products.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        await testimonials_collection.insert_many(testimonials_data)
        logger.info("Testimonials initialized")

    # Advantages (Why Choose Us)
    advantages_collection = db.advantages
    if await advantages_collection.count_documents({}) == 0:
        advantages_data = [
            {
                "title": "UAE Freezone Licensed Company (RAKEZ)",
                "description": "Fully licensed and regulated by Ras Al Khaimah Economic Zone",
                "icon": "Shield",
                "order": 1,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "title": "Global Export & Shipping",
                "description": "Worldwide delivery with reliable logistics partners",
                "icon": "Globe",
                "order": 2,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "title": "Wide Product Range",
                "description": "Comprehensive inventory from cars to heavy machinery",
                "icon": "Package",
                "order": 3,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "title": "Reliable Sourcing & Fast Delivery",
                "description": "Trusted suppliers and efficient delivery systems",
                "icon": "Truck",
                "order": 4,
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        await advantages_collection.insert_many(advantages_data)
        logger.info("Advantages initialized")