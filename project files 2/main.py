from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Product, UserInteraction, RecommendationResponse
from database import db, get_db
from recommendation import RecommendationEngine
import uuid

app = FastAPI(title="AuraCart AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_connected = False

@app.get("/")
async def root():
    return {
        "message": "AuraCart AI API is running",
        "status": "online",
        "database": "MongoDB (Live)" if mongo_connected else "In-Memory (Mock Mode)"
    }

@app.on_event("startup")
async def startup_db_client():
    global recommender, mongo_connected
    products_list = []
    
    mock_products = [
        {"_id": "1", "name": "Aura Glow Watch", "description": "Premium smart watch with OLED display", "price": 199.99, "category": "Electronics", "image_url": "/images/gadget_watch_premium_1775454756031.png", "tags": ["smart", "luxury"]},
        {"_id": "2", "name": "Nebula Headphones", "description": "Noise cancelling wireless headphones", "price": 299.99, "category": "Electronics", "image_url": "/images/headphones.jpg", "tags": ["audio", "wireless"]},
        {"_id": "3", "name": "Zenith Laptop", "description": "Ultra-thin high performance laptop", "price": 1299.99, "category": "Computers", "image_url": "/images/laptop.jpg", "tags": ["productivity", "sleek"]},
        {"_id": "4", "name": "Titan Gaming Mouse", "description": "Ergonomic RGB gaming mouse", "price": 59.99, "category": "Accessories", "image_url": "/images/mouse.jpg", "tags": ["gaming", "performance"]},
        {"_id": "5", "name": "Echo Smart Speaker", "description": "AI-powered smart home assistant", "price": 89.99, "category": "Electronics", "image_url": "/images/speaker.jpg", "tags": ["smart", "audio"]},
    ]

    try:
        if db is not None:
            # Check if DB is alive
            await db.command("ping")
            count = await db.products.count_documents({})
            if count == 0:
                await db.products.insert_many(mock_products)
            
            products_cursor = db.products.find()
            async for p in products_cursor:
                products_list.append(Product(**p))
            mongo_connected = True
            print("Connected to MongoDB successfully.")
        else:
            raise ConnectionError("Database object is None")
    except Exception as e:
        print(f"MongoDB not found or connection failed. Falling back to in-memory mode. Error: {e}")
        products_list = [Product(**p) for p in mock_products]

    recommender = RecommendationEngine(products_list)
    # Store globally for routes to use fallback
    app.state.products = products_list

@app.get("/products", response_model=List[Product])
async def get_products():
    try:
        products = []
        async for p in db.products.find():
            products.append(Product(**p))
        return products
    except Exception:
        return app.state.products

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        product = await db.products.find_one({"_id": product_id})
        if product:
            return Product(**product)
    except Exception:
        pass
    
    # Fallback search
    for p in app.state.products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/interactions")
async def track_interaction(interaction: UserInteraction):
    try:
        await db.interactions.insert_one(interaction.dict())
        return {"status": "success"}
    except Exception:
        # Silently fail for mock mode
        return {"status": "success", "mode": "mock"}

@app.get("/recommendations/{user_id}", response_model=List[Product])
async def get_recommendations(user_id: str):
    try:
        # Fetch recent interactions for user
        interactions_cursor = db.interactions.find({"user_id": user_id}).sort("timestamp", -1).limit(20)
        interactions = []
        async for i in interactions_cursor:
            interactions.append(i)
        
        reccs = recommender.get_user_recommendations(interactions)
        return reccs
    except Exception:
        return recommender.get_user_recommendations([]) # Fallback to generic

@app.get("/products/{product_id}/similar", response_model=List[Product])
async def get_similar_products(product_id: str):
    reccs = recommender.get_similar_products(product_id)
    return reccs
