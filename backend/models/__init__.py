"""
SQLAlchemy models for Watch Tower
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, ForeignKey, DECIMAL, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

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
    vpc_id = Column(String(100), unique=True)
    loconav_trip_id = Column(String(100), unique=True)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"))
    status = Column(String(50), default="scheduled")
    
    # Relationships
    truck = relationship("Truck", back_populates="trips")

class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"))
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(DECIMAL(5, 2))
    heading = Column(Integer)
    ignition = Column(Boolean)
    
    # Relationships
    truck = relationship("Truck", back_populates="positions")
