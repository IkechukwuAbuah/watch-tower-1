# Watch Tower - Data Dictionary

## 1. Core Entities

### Trucks
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| truck_number | VARCHAR(50) | Unique truck identifier | T11985LA |
| loconav_vehicle_id | VARCHAR(100) | LocoNav system ID | 077c6ab2-6456-4e07-abd6 |
| company | VARCHAR(100) | Operating company | FM, VPC, LH, PC |
| fleet_manager | VARCHAR(100) | Manager name | SEYE |
| status | VARCHAR(50) | Operational status | operational, maintenance |
| brand | VARCHAR(50) | Truck manufacturer | MACK, Volvo |
| trailer_size | VARCHAR(20) | Container size | 40FT, 20FT |
| operating_location | VARCHAR(100) | Base location | ESSLIBRA TERMINAL |

### Drivers
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| name | VARCHAR(255) | Driver full name | Moruf Fatai |
| phone | VARCHAR(20) | Phone number | 08037813632 |
| has_smartphone | BOOLEAN | Smartphone ownership | false |
| truck_id | UUID | Assigned truck | FK to trucks |

### Locations
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| name | VARCHAR(255) | Location name | ESSLIBRA Ibeshe |
| type | VARCHAR(50) | Location category | terminal, client |
| address | TEXT | Full address | Plot 1, Terminal Road, Ibeshe |
| coordinates | POINT | GPS coordinates | (6.556389, 3.475556) |
| geofence_id | INTEGER | LocoNav geofence ID | 12345 |
| city | VARCHAR(100) | City name | Lagos |
| state | VARCHAR(100) | State name | Lagos |

### Organizations
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| name | VARCHAR(255) | Company name | Deekay Group |
| type | VARCHAR(50) | Organization type | client, transporter |
| email | VARCHAR(255) | Contact email | logistics@deekaygroup.com |
| phone | VARCHAR(20) | Contact phone | 09062902926 |
| sales_manager | VARCHAR(255) | Assigned sales manager | ANITA |

### Trips
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| vpc_id | VARCHAR(100) | VPC trip identifier | 01/Apr/2025-T11985LA-CA60 |
| loconav_trip_id | VARCHAR(100) | LocoNav system ID | trip_12345 |
| truck_id | UUID | Assigned truck | FK to trucks |
| driver_id | UUID | Assigned driver | FK to drivers |
| client_id | UUID | Client organization | FK to organizations |
| pickup_location_id | UUID | Source location | FK to locations |
| delivery_location_id | UUID | Destination | FK to locations |
| container_no | VARCHAR(50) | Container number | TCNU3877560 |
| cargo_type | VARCHAR(50) | Cargo description | 40FT, Empty For Export |
| weight_tons | DECIMAL(10,2) | Cargo weight | 5.00 |
| status | VARCHAR(50) | Trip status | scheduled, ongoing, completed |
| scheduled_departure | TIMESTAMP | Planned departure | 2025-04-01 08:00:00 |
| actual_departure | TIMESTAMP | Actual departure | 2025-04-01 08:34:00 |
| arrival_time | TIMESTAMP | Arrival at destination | 2025-04-02 05:41:00 |
| offload_time | TIMESTAMP | Offloading complete | 2025-04-02 11:21:00 |

## 2. Tracking Data

### Vehicle Positions
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| truck_id | UUID | Vehicle reference | FK to trucks |
| timestamp | TIMESTAMP | Position time | 2025-04-01 12:30:45 |
| coordinates | POINT | GPS location | (6.5244, 3.3792) |
| speed | DECIMAL(5,2) | Speed in km/h | 45.50 |
| heading | INTEGER | Direction degrees | 180 |
| ignition | BOOLEAN | Engine status | true |

### Alerts
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| truck_id | UUID | Vehicle reference | FK to trucks |
| alert_type | VARCHAR(50) | Alert category | overspeed, geofence_entry |
| timestamp | TIMESTAMP | Event time | 2025-04-01 14:15:00 |
| location | POINT | Event location | (6.5244, 3.3792) |
| details | JSONB | Additional data | {"speed": 85, "limit": 60} |

## 3. Analytics

### Daily Metrics
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| date | DATE | Metric date | 2025-04-01 |
| total_trips | INTEGER | Trips count | 45 |
| completed_trips | INTEGER | Successful trips | 42 |
| average_tat_hours | DECIMAL(10,2) | Avg turnaround time | 28.5 |
| fleet_utilization_percent | DECIMAL(5,2) | Active trucks % | 78.5 |
| total_distance_km | DECIMAL(10,2) | Distance traveled | 3450.75 |

### Truck Performance
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| truck_id | UUID | Vehicle reference | FK to trucks |
| period_start | DATE | Period beginning | 2025-04-01 |
| period_end | DATE | Period end | 2025-04-07 |
| trips_completed | INTEGER | Successful trips | 12 |
| total_distance_km | DECIMAL(10,2) | Distance covered | 890.5 |
| average_tat_hours | DECIMAL(10,2) | Avg turnaround | 26.3 |
| idle_time_hours | DECIMAL(10,2) | Idle duration | 15.5 |

## 4. System Data

### Sync Status
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| table_name | VARCHAR(100) | Table synced | trucks |
| last_sync | TIMESTAMP | Last sync time | 2025-04-01 12:00:00 |
| records_synced | INTEGER | Records count | 84 |
| status | VARCHAR(50) | Sync status | success, failed |
| error_message | TEXT | Error details | null |

### API Logs
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| endpoint | VARCHAR(255) | API endpoint | /api/v1/trips |
| method | VARCHAR(10) | HTTP method | POST |
| user_id | UUID | Requesting user | FK to users |
| timestamp | TIMESTAMP | Request time | 2025-04-01 14:30:00 |
| response_code | INTEGER | HTTP status | 200 |
| response_time_ms | INTEGER | Processing time | 245 |

## 5. Enumerations

### Trip Status
- `scheduled` - Trip created, not started
- `ongoing` - Trip in progress
- `delayed` - Behind schedule
- `completed` - Successfully finished
- `cancelled` - Trip cancelled
- `failed` - Could not complete

### Alert Types
- `geofence_entry` - Entered location
- `geofence_exit` - Left location
- `overspeed` - Speed limit exceeded
- `harsh_braking` - Sudden brake
- `harsh_acceleration` - Rapid acceleration
- `idle` - Extended idle time
- `device_offline` - GPS offline

### Truck Status
- `operational` - Available for trips
- `en_route` - On active trip
- `maintenance` - Under repair
- `idle` - Not assigned
- `offline` - No GPS signal

### Location Types
- `terminal` - Port/terminal
- `client` - Customer location
- `service_area` - Fuel/rest stop
- `depot` - Parking area

### Cargo Types
- `40FT` - 40-foot container
- `20FT` - 20-foot container
- `Empty For Export` - Empty container
- `Import` - Loaded import
- `Export` - Loaded export

## 6. Business Rules

### Trip Creation
- Pickup and delivery locations must have valid geofences
- Scheduled time must be at least 30 minutes in future
- Truck must be in 'operational' status
- Driver must be assigned to truck

### Geofence Rules
- Radius: 50m - 300m
- Entry/exit tracked only during active trips
- 5-minute dwell time for valid entry

### Alert Thresholds
- Overspeed: >60 km/h
- Idle: >20 minutes with ignition on
- Delay: 2+ hours after scheduled departure
- Harsh brake: -8 m/s²
- Harsh acceleration: +7 m/s²

### Data Retention
- GPS positions: 30 days
- Trip records: 6 months
- Analytics: 12 months
- Alerts: 90 days
