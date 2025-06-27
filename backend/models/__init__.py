"""
SQLAlchemy models for Watch Tower
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, DECIMAL, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography
import uuid
from datetime import datetime

# Import Base from session.py to ensure consistency
from db.session import Base

class Truck(Base):
    __tablename__ = "trucks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    truck_number = Column(String(50), unique=True, nullable=False)
    loconav_vehicle_id = Column(String(100), unique=True)
    company = Column(String(100))
    fleet_manager = Column(String(100))
    status = Column(String(50), default="operational")
    brand = Column(String(50))
    trailer_size = Column(String(20))
    operating_location = Column(String(100))
    
    # Relationships
    trips = relationship("Trip", back_populates="truck")
    positions = relationship("VehiclePosition", back_populates="truck")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vpc_id = Column(String(100), unique=True, nullable=False)
    loconav_trip_id = Column(String(100), unique=True)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"), nullable=False, index=True)
    
    # Trip details
    status = Column(String(50), default="scheduled", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Origin and destination as PostGIS geography points
    origin_location = Column(Geography('POINT', srid=4326))
    destination_location = Column(Geography('POINT', srid=4326))
    
    # Address information
    origin_address = Column(Text)
    destination_address = Column(Text)
    
    # Trip metadata
    distance_km = Column(DECIMAL(8, 2))
    estimated_duration_minutes = Column(Integer)
    
    # Relationships
    truck = relationship("Truck", back_populates="trips")

class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # PostGIS geography point for efficient spatial queries
    location = Column(Geography('POINT', srid=4326), nullable=False, index=True)
    
    # Vehicle telemetry
    speed = Column(DECIMAL(5, 2))  # km/h
    heading = Column(Integer)  # degrees (0-359)
    ignition = Column(Boolean)
    
    # Additional tracking data
    altitude = Column(DECIMAL(8, 2))  # meters
    accuracy = Column(DECIMAL(6, 2))  # meters
    
    # Relationships
    truck = relationship("Truck", back_populates="positions")
