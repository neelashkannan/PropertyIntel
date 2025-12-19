from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import uuid
from pathlib import Path

from database import get_db, engine, SessionLocal
from models import User, Property, PropertyMedia
from schemas import (
    UserCreate, UserLogin, UserResponse,
    PropertyCreate, PropertyUpdate, PropertyResponse,
    PropertyAnalysis, Token
)
from auth import create_access_token, verify_token, get_password_hash, verify_password
from services.property_service import PropertyService
from services.analysis_service import AnalysisService
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

# Create tables
import models
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Purva.ai Property Intelligence API",
    description="Professional Property Intelligence Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Load postcode data
try:
    postcode_df = pd.read_csv("../postcode_to_datazone.csv")
    postcode_df["Postcode"] = postcode_df["Postcode"].str.strip().str.upper().str.replace(" ", "")
except Exception:
    # Fallback to empty DataFrame if file missing in dev
    postcode_df = pd.DataFrame({"Postcode": [], "DataZone2011Code": []})


def ensure_default_admin():
    """Create a default admin user in development if enabled and absent."""
    enabled = os.getenv("ENABLE_DEFAULT_ADMIN", "true").lower() in {"1", "true", "yes"}
    if not enabled:
        return

    # Use proper email format for admin user
    default_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@local.com")
    default_name = os.getenv("DEFAULT_ADMIN_NAME", "Administrator")
    default_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin123")

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == default_email).first()
        if existing:
            print(f"Admin user already exists: {default_email}")
            return
        user = User(
            email=default_email,
            full_name=default_name,
            hashed_password=get_password_hash(default_password),
        )
        db.add(user)
        db.commit()
        print(f"Created default admin user: {default_email} with password: {default_password}")
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    ensure_default_admin()

# Dependency injection for services
def get_property_service(db: Session = Depends(get_db)) -> PropertyService:
    return PropertyService(db)

def get_analysis_service(db: Session = Depends(get_db)) -> AnalysisService:
    return AnalysisService(db)

# Auth endpoints
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        access_token=access_token,
        token_type="bearer"
    )

@app.post("/api/auth/login", response_model=UserResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        access_token=access_token,
        token_type="bearer"
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

# Property endpoints
@app.get("/api/properties", response_model=List[PropertyResponse])
async def get_properties(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    properties = db.query(Property).filter(Property.user_id == current_user.id).all()
    return properties

@app.post("/api/properties", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get datazone from postcode
    postcode_clean = property_data.postcode.strip().upper().replace(" ", "")
    dz_match = postcode_df[postcode_df["Postcode"] == postcode_clean]
    datazone = dz_match.iloc[0]["DataZone2011Code"] if not dz_match.empty else None
    
    property_dict = property_data.model_dump()
    property_dict.update({
        "user_id": current_user.id,
        "datazone": datazone,
        "created_at": datetime.utcnow()
    })
    
    property_obj = Property(**property_dict)
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    
    return property_obj

@app.get("/api/properties/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.user_id == current_user.id
    ).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_obj

@app.put("/api/properties/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.user_id == current_user.id
    ).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Update fields
    for field, value in property_data.model_dump(exclude_unset=True).items():
        setattr(property_obj, field, value)
    
    property_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(property_obj)
    
    return property_obj

@app.delete("/api/properties/{property_id}")
async def delete_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.user_id == current_user.id
    ).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    db.delete(property_obj)
    db.commit()
    
    return {"message": "Property deleted successfully"}

@app.post("/api/properties/{property_id}/upload")
async def upload_property_media(
    property_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.user_id == current_user.id
    ).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    uploaded_files = []
    media_dir = Path(f"media/{current_user.id}/{property_id}")
    media_dir.mkdir(parents=True, exist_ok=True)
    
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = media_dir / f"{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Save to database
        media = PropertyMedia(
            property_id=property_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            mime_type=file.content_type
        )
        db.add(media)
        uploaded_files.append(file.filename)
    
    db.commit()
    
    return {"uploaded_files": uploaded_files}

@app.post("/api/properties/analyze", response_model=PropertyAnalysis)
async def analyze_properties(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    properties = db.query(Property).filter(Property.user_id == current_user.id).all()
    
    if not properties:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No properties found for analysis"
        )
    
    # Use PropertyService to get the analysis
    property_service = PropertyService(db)
    analysis_result = property_service.analyze_portfolio(current_user.id)
    
    return analysis_result

@app.get("/")
async def root():
    return {
        "message": "Purva.ai API",
        "version": "1.0.0",
        "description": "Professional Property Intelligence Platform"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
