from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import os
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client.task_db

# Security
security = HTTPBearer()

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime

# Dependency for MongoDB
def get_db():
    try:
        yield db
    finally:
        pass  # MongoDB client closes automatically

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    token = credentials.credentials
    # Simple token check (in real app, validate against stored tokens)
    user = db.users.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user["_id"]

# Create User Endpoint
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db=Depends(get_db)):
    logger.info(f"Creating user with email: {user.email}")
    
    # Check if user exists
    if db.users.find_one({"email": user.email}):
        logger.error(f"User with email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user document
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": user.password,  # In production, hash the password
        "created_at": datetime.utcnow(),
        "deleted_at": None
    }
    
    # Insert into MongoDB
    result = db.users.insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    
    logger.info(f"User created with ID: {user_data['id']}")
    return UserResponse(**user_data)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    logger.info(f"Login attempt for email: {request.email}")
    user = db.users.find_one({"email": request.email, "password": request.password})
    if not user:
        logger.error("Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate and store token
    token = secrets.token_hex(16)
    db.users.update_one({"_id": user["_id"]}, {"$set": {"token": token}})
    logger.info(f"Login successful for user: {request.email}")
    return {"token": token}