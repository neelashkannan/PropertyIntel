from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    properties = relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Address
    house_number = Column(String, nullable=False)
    street_name = Column(String, nullable=False)
    postcode = Column(String, nullable=False, index=True)
    datazone = Column(String, index=True)
    
    # Property details
    property_type = Column(String, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    size_sqft = Column(Integer)
    floor_number = Column(Integer)
    
    # Features
    new_build = Column(String)
    solar_panels = Column(String)
    epc_rating = Column(String)
    council_tax_band = Column(String)
    parking = Column(String)
    parking_type = Column(String)
    garden = Column(String)
    garden_type = Column(String)
    lift_available = Column(String)
    
    # Extras
    sunroom = Column(Boolean, default=False)
    basement = Column(Boolean, default=False)
    loft = Column(Boolean, default=False)
    parking_additional = Column(Boolean, default=False)
    
    # Additional info
    misc_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    media = relationship(
        "PropertyMedia",
        back_populates="property",
        cascade="all, delete-orphan",
    )

class PropertyMedia(Base):
    __tablename__ = "property_media"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="media")
