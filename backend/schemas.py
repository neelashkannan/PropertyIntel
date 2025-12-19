from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True

# Property schemas
class PropertyCreate(BaseModel):
    house_number: str
    street_name: str
    postcode: str
    property_type: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    size_sqft: Optional[int] = None
    floor_number: Optional[int] = None
    new_build: Optional[str] = None
    solar_panels: Optional[str] = None
    epc_rating: Optional[str] = None
    council_tax_band: Optional[str] = None
    parking: Optional[str] = None
    parking_type: Optional[str] = None
    garden: Optional[str] = None
    garden_type: Optional[str] = None
    lift_available: Optional[str] = None
    sunroom: Optional[bool] = False
    basement: Optional[bool] = False
    loft: Optional[bool] = False
    parking_additional: Optional[bool] = False
    misc_notes: Optional[str] = None

class PropertyUpdate(PropertyCreate):
    pass

class PropertyResponse(PropertyCreate):
    id: int
    user_id: int
    datazone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Analysis schemas
class PropertyAnalysis(BaseModel):
    total_properties: int
    avg_epc_rating: Optional[str]
    total_value_estimate: Optional[float]
    recommendations: List[str]
    energy_efficiency_score: Optional[float]
    investment_score: Optional[float]
    risk_assessment: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str