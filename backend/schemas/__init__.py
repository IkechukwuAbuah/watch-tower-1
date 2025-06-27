"""
Pydantic schemas for Watch Tower API
Provides request/response validation and OpenAPI documentation
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic.types import condecimal, conint


# Base schemas
class TimestampedSchema(BaseModel):
    """Base schema with timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LocationSchema(BaseModel):
    """Schema for geographic location with validation"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    
    @field_validator('latitude', 'longitude')
    @classmethod
    def validate_coordinates(cls, v: float) -> float:
        """Validate coordinate precision"""
        if not isinstance(v, (int, float)):
            raise ValueError('Coordinates must be numeric')
        # Round to 6 decimal places (~1 meter precision)
        return round(float(v), 6)

    def to_wkt(self) -> str:
        """Convert to Well-Known Text format for PostGIS"""
        return f"POINT({self.longitude} {self.latitude})"


class GeoJSONPointSchema(BaseModel):
    """GeoJSON Point representation"""
    type: str = Field(default="Point", description="GeoJSON type")
    coordinates: Tuple[float, float] = Field(..., description="[longitude, latitude]")
    
    @field_validator('coordinates')
    @classmethod
    def validate_coordinates(cls, v: Tuple[float, float]) -> Tuple[float, float]:
        """Validate longitude, latitude order"""
        if len(v) != 2:
            raise ValueError('Coordinates must be [longitude, latitude]')
        lon, lat = v
        if not (-180 <= lon <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        if not (-90 <= lat <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        return (round(lon, 6), round(lat, 6))


# Truck schemas
class TruckBase(BaseModel):
    """Base truck schema with common fields"""
    truck_number: str = Field(..., min_length=1, max_length=50, description="Unique truck identifier")
    loconav_vehicle_id: Optional[str] = Field(None, max_length=100, description="LocoNav vehicle ID")
    company: Optional[str] = Field(None, max_length=100, description="Operating company")
    fleet_manager: Optional[str] = Field(None, max_length=100, description="Fleet manager name")
    status: str = Field(default="operational", max_length=50, description="Truck status")
    brand: Optional[str] = Field(None, max_length=50, description="Truck brand/make")
    trailer_size: Optional[str] = Field(None, max_length=20, description="Trailer size (20ft, 40ft)")
    operating_location: Optional[str] = Field(None, max_length=100, description="Primary operating area")


class TruckCreate(TruckBase):
    """Schema for creating a new truck"""
    pass


class TruckUpdate(BaseModel):
    """Schema for updating a truck (all fields optional)"""
    truck_number: Optional[str] = Field(None, min_length=1, max_length=50)
    loconav_vehicle_id: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    fleet_manager: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    trailer_size: Optional[str] = Field(None, max_length=20)
    operating_location: Optional[str] = Field(None, max_length=100)


class TruckResponse(TruckBase, TimestampedSchema):
    """Schema for truck API responses"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Unique truck ID")


# Trip schemas
class TripBase(BaseModel):
    """Base trip schema with common fields"""
    vpc_id: str = Field(..., min_length=1, max_length=100, description="VPC trip identifier")
    loconav_trip_id: Optional[str] = Field(None, max_length=100, description="LocoNav trip ID")
    status: str = Field(default="scheduled", max_length=50, description="Trip status")
    origin_address: Optional[str] = Field(None, description="Origin address")
    destination_address: Optional[str] = Field(None, description="Destination address")
    distance_km: Optional[condecimal(max_digits=8, decimal_places=2)] = Field(None, description="Distance in kilometers")
    estimated_duration_minutes: Optional[conint(ge=0)] = Field(None, description="Estimated duration in minutes")


class TripCreate(TripBase):
    """Schema for creating a new trip"""
    truck_id: UUID = Field(..., description="ID of assigned truck")
    origin_location: Optional[LocationSchema] = Field(None, description="Origin coordinates")
    destination_location: Optional[LocationSchema] = Field(None, description="Destination coordinates")


class TripUpdate(BaseModel):
    """Schema for updating a trip"""
    vpc_id: Optional[str] = Field(None, min_length=1, max_length=100)
    loconav_trip_id: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    origin_location: Optional[LocationSchema] = None
    destination_location: Optional[LocationSchema] = None
    origin_address: Optional[str] = None
    destination_address: Optional[str] = None
    distance_km: Optional[condecimal(max_digits=8, decimal_places=2)] = None
    estimated_duration_minutes: Optional[conint(ge=0)] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TripResponse(TripBase, TimestampedSchema):
    """Schema for trip API responses"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Unique trip ID")
    truck_id: UUID = Field(..., description="ID of assigned truck")
    started_at: Optional[datetime] = Field(None, description="Trip start time")
    completed_at: Optional[datetime] = Field(None, description="Trip completion time")
    
    # GeoJSON representations for frontend
    origin_geojson: Optional[GeoJSONPointSchema] = Field(None, description="Origin as GeoJSON")
    destination_geojson: Optional[GeoJSONPointSchema] = Field(None, description="Destination as GeoJSON")


# Vehicle Position schemas
class VehiclePositionBase(BaseModel):
    """Base vehicle position schema"""
    timestamp: datetime = Field(..., description="Position timestamp")
    speed: Optional[condecimal(max_digits=5, decimal_places=2)] = Field(None, description="Speed in km/h")
    heading: Optional[conint(ge=0, le=359)] = Field(None, description="Heading in degrees (0-359)")
    ignition: Optional[bool] = Field(None, description="Ignition status")
    altitude: Optional[condecimal(max_digits=8, decimal_places=2)] = Field(None, description="Altitude in meters")
    accuracy: Optional[condecimal(max_digits=6, decimal_places=2)] = Field(None, description="GPS accuracy in meters")


class VehiclePositionCreate(VehiclePositionBase):
    """Schema for creating a vehicle position record"""
    truck_id: UUID = Field(..., description="ID of the truck")
    location: LocationSchema = Field(..., description="GPS coordinates")


class VehiclePositionResponse(VehiclePositionBase):
    """Schema for vehicle position API responses"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Unique position ID")
    truck_id: UUID = Field(..., description="ID of the truck")
    
    # GeoJSON representation
    location_geojson: GeoJSONPointSchema = Field(..., description="Location as GeoJSON")


# Webhook schemas
class LocoNavWebhookPayload(BaseModel):
    """Schema for LocoNav webhook payload"""
    vehicle_id: str = Field(..., description="LocoNav vehicle ID")
    timestamp: datetime = Field(..., description="Position timestamp")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed: Optional[float] = Field(None, ge=0, description="Speed in km/h")
    heading: Optional[int] = Field(None, ge=0, le=359)
    ignition: Optional[bool] = None
    altitude: Optional[float] = None
    accuracy: Optional[float] = Field(None, ge=0)
    
    # Additional LocoNav specific fields
    event_type: Optional[str] = Field(None, description="Event type from LocoNav")
    trip_id: Optional[str] = Field(None, description="LocoNav trip ID")


# Analytics schemas
class DailyMetricsResponse(BaseModel):
    """Schema for daily metrics response"""
    date: datetime = Field(..., description="Date for metrics")
    total_trucks: int = Field(..., description="Total number of trucks")
    active_trucks: int = Field(..., description="Number of active trucks")
    total_trips: int = Field(..., description="Total trips on this date")
    completed_trips: int = Field(..., description="Completed trips")
    total_distance_km: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Total distance traveled")
    average_speed_kmh: condecimal(max_digits=5, decimal_places=2) = Field(..., description="Average speed")
    fuel_efficiency_score: Optional[condecimal(max_digits=3, decimal_places=1)] = Field(None, description="Fuel efficiency score (0-10)")


class TruckMetricsResponse(BaseModel):
    """Schema for per-truck metrics response"""
    truck_id: UUID = Field(..., description="Truck ID")
    truck_number: str = Field(..., description="Truck number")
    date: datetime = Field(..., description="Date for metrics")
    distance_km: condecimal(max_digits=8, decimal_places=2) = Field(..., description="Distance traveled")
    trips_count: int = Field(..., description="Number of trips")
    active_hours: condecimal(max_digits=4, decimal_places=1) = Field(..., description="Active hours")
    average_speed_kmh: condecimal(max_digits=5, decimal_places=2) = Field(..., description="Average speed")
    max_speed_kmh: condecimal(max_digits=5, decimal_places=2) = Field(..., description="Maximum speed")


# Query parameter schemas
class TruckQueryParams(BaseModel):
    """Query parameters for truck listing"""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of records to return")
    status: Optional[str] = Field(None, description="Filter by truck status")
    company: Optional[str] = Field(None, description="Filter by company")
    location: Optional[str] = Field(None, description="Filter by operating location")


class TripQueryParams(BaseModel):
    """Query parameters for trip listing"""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of records to return")
    status: Optional[str] = Field(None, description="Filter by trip status")
    truck_id: Optional[UUID] = Field(None, description="Filter by truck ID")
    date_from: Optional[datetime] = Field(None, description="Filter trips from this date")
    date_to: Optional[datetime] = Field(None, description="Filter trips to this date")


# Error schemas
class ErrorResponse(BaseModel):
    """Standard error response schema"""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    code: Optional[str] = Field(None, description="Error code")


# Success schemas
class SuccessResponse(BaseModel):
    """Standard success response schema"""
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Optional response data")


# Export all schemas
__all__ = [
    # Base schemas
    "TimestampedSchema",
    "LocationSchema", 
    "GeoJSONPointSchema",
    # Truck schemas
    "TruckBase",
    "TruckCreate",
    "TruckUpdate", 
    "TruckResponse",
    # Trip schemas
    "TripBase",
    "TripCreate",
    "TripUpdate",
    "TripResponse",
    # Position schemas
    "VehiclePositionBase",
    "VehiclePositionCreate",
    "VehiclePositionResponse",
    # Webhook schemas
    "LocoNavWebhookPayload",
    # Analytics schemas
    "DailyMetricsResponse",
    "TruckMetricsResponse",
    # Query schemas
    "TruckQueryParams",
    "TripQueryParams",
    # Standard responses
    "ErrorResponse",
    "SuccessResponse"
]