# [PROD] Loconav Developer APIs

# LocoNav Integration Documentation

Welcome to LocoNav's comprehensive set of REST APIs and webhooks, designed to seamlessly integrate LocoNav's robust solutions into your platform. Our APIs cover key areas such as telematics, safety, connected driver features,and more, empowering partners to track, trace, and manage assets efficiently.

# Types of APIs

# CRUD APIs

CRUD (Create, Read, Update, Delete) APIs provide basic operations for managing resources.

# Telematics APIs

Telematics APIs offer access to sensor data, GPS locations, videos, and live streams related to vehicles.

# Webhooks

Webhooks facilitate real-time notifications for alerts and live location updates.

Alerts : Receive real-time notifications for various alerts such as speeding, geofence violations, etc via Alert webhooks.

GPS Live Locations : Get instant updates on the live locations of vehicles or assets via location webhooks.

# Base URLs

api.a.loconav.com for Global customers

sa.loconav.com for KSA customers

om.loconav.com for OMAN customers

np.loconav.com for NEPAL customers

# Authentication

# Mechanism

To access LocoNav APIs, use the User Token provided for user-level authentication. Each user in our system is assigned a unique auth token. For your specific token details and access to the live token and testing environment,please reach out to your designated LocoNav point of contact (SPOC).

Header Name: User-Authentication

# Obtaining Authentication Token

To obtain your authentication token and details for testing environments, kindly get in touch with your LocoNav SPOC. They will assist you in acquiring the necessary credentials for a secure and seamless integration.

# Notes for API Usage

1. Time Requirement: APIs that utilize time ranges or time parameters like startTime and endTime in requests necessitate the use of Epoch timestamps in seconds exclusively.

2. Authentication Handling: Users will receive a 401 Unauthorized response if authentication credentials are incorrect or not provided properly in the request headers.

3. Pagination Requirement: All listing APIs are paginated, and a pagination object must be included in requests to navigate through pages effectively.

4. Rate Limiting: Each API endpoint is subject to rate limiting. If an API is called more than 500 times within a 60-second rolling window, it will be throttled, and a 429 Too Many Requests error will be returned to prevent abuse and ensure fair usage.

Conact the Developer at developers@loconav.com

# Drivers

Efficient driver management is essential for the optimal operation of a fleet.

Leveraging the capabilities of LocoNav REST APIs, fleet managers can seamlessly create, update,and retrieve detailed information about drivers. The system allows for precise retrieval of driver details based on their names, enabling informed decision-making.

Moreover, fleet managers can maintain the accuracy of their driver roster by securely deleting off record drivers. This suite of features empowers fleet managers to maintain a well-organized and high-performing team, enhancing overall fleet management effectiveness.

## GETGet Driver

https://api.a.loconav.com/integration/api/v1/drivers/{{driverId}}

# Overview

The Driver Details API allows users to retrieve detailed information about a specific driver in the LocoNav system.This information includes the driver's personal details, contact information, license details, guarantor information,and uploaded documents.

## Path Parameters

driverId (integer, required): The unique identifier of the driver for which details are requested.

# Response Body

id (integer): The unique identifier of the driver.

name (string): The name of the driver.

phoneNumber (string): The phone number of the driver.

aadharNumber (string): The Aadhar number of the driver (if available).

vehicleNumber (string): The vehicle number assigned to the driver.

licenseNumber (string): The driver's license number.

guarantorName (string): The name of the driver's guarantor.

guarantorPhoneNumber (string): The phone number of the driver's guarantor.

licenseIssueDate (integer): The timestamp of the driver's license issue date.

licenseValidFrom (integer): The timestamp of the start date of the driver's license validity.

licenseValidUpto (integer): The timestamp of the end date of the driver's license validity.

driverCountryCode (string): The country code of the driver.

guarantorCountryCode (string): The country code of the driver's guarantor.

rfidTrackingId (string): The RFID tracking ID associated with the driver (if available).

uploads (object): An object containing uploaded documents related to the driver.

driversLicense (array): An array of objects representing uploaded driver's license documents.

image (string): The URL to view the uploaded image of the driver's license.

id (integer): The unique identifier of the uploaded document.

fileName (string): The name of the uploaded file.

## HEADERS

User-Authentication {{auth-token}}

# GETList drivers (Filter)

https://api.a.loconav.com/integration/api/v1/drivers?name={{driverName}}&page=1&perPage=10

# Overview

The Search Drivers API allows users to search for drivers by name. Users can provide a partial or full name of the driver to retrieve a list of matching drivers along with their associated phone numbers.

# Request Parameters

name (string): The name of the driver to search for. This parameter supports partial or full name matching.

page (integer): The page number of the results to retrieve. Default is 1.

perPage (integer): The number of results per page. Default is 10.

getIdAndName (boolean,optional) default true, for more details set it false

vehicleIds: comma seprated vehicle uuid's

# Response Structure

values (array): Array containing driver objects matching the search query.

id (integer): Unique identifier for the driver.

name (string): Name of the driver.

phone_number (string): Phone number of the driver.

pagination (object): Pagination details.

page (integer): Current page number.

perPage (integer): Number of results per page.

more (boolean): Indicates whether there are more pages of data available.

metadata (object): Additional metadata if available.

# Note

The name parameter supports partial or full name matching, allowing users to search for drivers based on various name combinations.

## HEADERS

User-Authentication {{auth-token}}

PARAMS

name {{driverName}}

Driver Name (type: String) (Require)

page 1

Page index (type: Integer) (optional, default: 1)

perPage 10

No of items per page (type: Integer) (optional, default: 10)

## POSTCreate Drivers

https://api.a.loconav.com/integration/api/v1/drivers

## Overview

The Create Driver API allows users to create a new driver profile by providing the driver's name, country code, and phone number.

# Request Body

name (string): The name of the driver.

countryCode (string): The country code associated with the driver's phone number.

phoneNumber (string): The phone number of the driver.

# Response Structure

success (boolean): Indicates whether the operation was successful.

data (object): Contains details of the created driver if the operation was successful.

id (integer): Unique identifier for the created driver.

name (string): Name of the created driver.

# Notes

The countryCode parameter should follow the ISO standard.

Phone numbers should be provided without any special characters (e.g., spaces, dashes)

# HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

# PUTUpdate Drivers

https://api.a.loconav.com/integration/api/v1/drivers/{{driverId}}

# Overview

The Update Driver API allows users to update the information of an

existing driver profile identified by the driver's unique identifier.

# Request Body

name (string): The updated name of the driver.

countryCode (string): The updated country code associated with the driver's phone number.

phoneNumber (string): The updated phone number of the driver.

# Response Structure

success (boolean): Indicates whether the operation was successful.

data (object): Contains details of the updated driver if the operation was successful.

id (integer): Unique identifier for the updated driver.

name (string): Updated name of the driver.

# Notes

The {driverId} parameter should be replaced with the actual unique identifier of the driver to be updated.

The countryCode parameter should follow the ISO standard.

Phone numbers should be provided without any special characters (e.g., spaces, dashes)

# HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

Body raw

{

"name": "demo",

"countryCode": "IN",

"phoneNumber": "8259986926"

}

# DELETEDelete Driver

https://api.a.loconav.com/integration/api/v1/drivers/{{driverId}}

# Overview

The Delete Driver API enables users to remove a driver profile from the system using the driver's unique identifier.

## Request Param

{driverId} : The unique identifier of the driver to be deleted.

# Response Structure

success (boolean): Indicates whether the operation was successful.

data (string): Confirmation message indicating that the driver was deleted successfully.

# Notes

The {driverId} parameter should be replaced with the actual unique identifier of the driver to be deleted.

Deleting a driver profile is irreversible. Ensure that the correct driver identifier is provided before executing the request.

# HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

<!-- POSTVehicle Assignment -->

https://api.a.loconav.com/integration/api/v1/driver_vehicle_assignments

# Overview

The Driver Vehicle Assignments API allows users to assign a driver to a specific vehicle in the LocoNav system. This association enables tracking and management of vehicles based on the assigned driver.

# Request Body

vehicleId (string, required): The unique identifier of the vehicle to be assigned to the driver.

driverId (integer, required): The unique identifier of the driver to be assigned to the vehicle.

# Response

Successful Response (200 OK)

## Status Codes

200 OK : The driver was successfully assigned to the vehicle.

404 Not Found : The specified vehicle was not found in the system.

## HEADERS

User-Authentication {{auth-token}}

Body raw (json)


| json<br>{<br> "vehicleId": "077c6ab2-6456-4e07-abd6-1e18bbe7ba1d",<br> "driverId": 29866<br>}<br><img src="https://web-api.textin.com/ocr_image/external/72ed100916f7847c.jpg"> |
| --- |


## PUTVehicle Unassignment

https://api.a.loconav.com/integration/api/v1/driver_vehicle_unassignments

## Overview

The Driver Vehicle Unassignments API allows users to remove the association of a driver from a specific vehicle in the LocoNav system. This action disassociates the driver from the vehicle for tracking and management purposes.

## Request Body

vehicleId (string, required): The unique identifier of the vehicle from which the driver will be unassigned.

driverId (integer, required): The unique identifier of the driver to be unassigned from the vehicle.

# Response

## Successful Response (200 OK)

# Status Codes

200 OK : The driver was successfully unassigned from the vehicle.

422 Unprocessable Entity : The specified driver is not currently assigned to the provided vehicle.

# HEADERS

User-Authentication {{auth-token}}

Body raw (json)


| json<br>{<br> "vehicleId": "077c6ab2-6456-4e07-abd6-1e18bbe7ba1d",  |
| --- |


"driverId": 29866

}

# Video Telematics VT

Video telematics APIs enable integration with video data captured by telematics systems in vehicles. These APIs provide access to various functionalities related to managing and analyzing video data, including live streaming, video recording, playback, and analytics.

Developers can use these APIs to build applications that leverage video footage for fleet management, driver monitoring, safety analysis, and more. By integrating video telematics APIs into their systems, businesses can enhance the efficiency, safety, and security of their operations on the road.

# Live Stream

# GETGet Livesteam

https://api.a.loconav.com/integration/api/v1/livestreams/{{sessionId}}

# Overview

This API retrieves the live video stream for vehicle telematics. It requires the session ID of the livestream.

## Query Parameters

sessionId (string): The session ID of the livestream.

# Request Headers

User-Authentication : Your user authentication token.

Content-Type : application/json

# Response

The API returns a JSON object with the following fields:

streamId (string): The ID of the video stream.

backCamUrl (string): URL for the back camera feed.

frontCamUrl (string): URL for the front camera feed.

options (array of strings): Available video options.

currentResolution (string): Current video resolution.

sessionId (string): The session ID of the livestream.

status (string): Status of the livestream (e.g., "active").

keepAliveInterval (integer): Interval for keeping the livestream alive.

totalSessionTime (integer): Total duration of the livestream session. (time in seconds)

activeSessions (integer): Number of active livestream sessions.

expiryNotificationBuffer (integer): Buffer time for expiry notification.

afterExpiryBuffer (integer): Buffer time after expiry.

## Notes

The livestream URLs ( backCamUrl and frontCamUrl ) should be used to access the video feeds.

Ensure that the session ID provided is valid and active.

Authentication token is required for accessing the livestream.

The response may contain additional fields not listed here.

## HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

## POSTCreate Livestream

<!-- https://api.a.loconav.com/integration/api/v1/livestreams -->

## Overview

This API initiates a live video streaming session for a vehicle. Data will be returned if vehicle support Video or contains active VT device.

## Request Body

vehicleId (string): The ID of the vehicle

resolution (string): The desired resolution for the video stream. Options

640x480

1280x720

# Response Structure

success (boolean): Indicates whether the request was successful or not.

data (object): Contains the details of the live video streaming session.

streamId (string): The ID of the video streaming session.

backCamUrl (string): URL for accessing the live stream from the back camera.

frontCamUrl (string): URL for accessing the live stream from the front camera.

options (array of strings): Available options for the video stream.

currentResolution (string): The current resolution of the video stream.

sessionId (string): The ID of the session.

status (string): The status of the session (e.g., initiated, active).

keepAliveInterval (integer): The interval (in seconds) for sending keep-alive signals.

totalSessionTime (integer): The total duration of the session (in seconds).

activeSessions (integer): The number of active sessions.

expiryNotificationBuffer (integer): The buffer time (in seconds) for expiry notification.

afterExpiryBuffer (integer): The buffer time (in seconds) after expiry.

# Notes

The resolution parameter specifies the desired resolution for the video stream.

The response provides URLs for accessing the live stream from the back and front cameras.

The status field indicates the status of the session, such as "initiated" or "active".

This API is used to initiate a live video streaming session for the specified vehicle's telematics data.

# HEADERS

User-Authentication {{auth-token}}

Body raw (json)


| json<br>{<br> "vehicleId": "ff3fb6bf-1c1e-429d-b5ac-60afda6ee94f",<br> "resolution": "640x480"<br>} |
| --- |


## PUTUpdate Livestream

https://api.a.loconav.com/integration/api/v1/livestreams/{{sessionId}}

# Overview

This API endpoint facilitates the modification of a livestream session, allowing users to either update its resolution or extend its duration.

# Request Body

operation (string): Indicates operation whether to update resolution or extend the livestream session.

Data Type: String

Options: "change_resolution" or "extend_duration"

resolution (string): Specifies the desired resolution for the livestream.

Data Type: String

Options: "640x480", "1280x720", "1920x1080", "3840x2160"

# Response Body

success (boolean): Indicates whether the request was successful.

Data Type: Boolean

message (string): Message confirming the success of the livestream session update.

Data Type: String

# HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

Body raw


| {<br> "operation": "extend_duration",<br> "resolution": "640x480"<br>} |
| --- |


# DELETEDelete Livestream

https://api.a.loconav.com/integration/api/v1/livestreams/{{streamId}}

# Overview

This API endpoint is used to delete a specific vehicle's telematics livestream by providing its unique session ID.

# Response Body

status (boolean): Indicates whether the request was successful.

Data Type: Boolean

data (object): Additional data related to the deletion process.

success (boolean): Indicates whether the deletion was successful.

Data Type: Boolean

message (string): A message confirming the success of the deletion operation.

Data Type: String

HEADERS

User-Authentication {{auth-token}}

# Videos

# GETGet Video

https://api.a.loconav.com/integration/api/v1/videos/{{voidId}}

# Overview

The Video Details API allows users to retrieve detailed information about a specific video recording, providing insights into the associated device, duration, format, creator type, and more.

# Request Headers

User-Authentication : The authentication token for accessing the API. Replace {{auth_token}} with the actual authentication token.

# Path Parameters

vodId (string, required): The unique identifier of the video on demand (VOD).

# Response Body

vodId (string): Unique identifier of the video on demand.

requestType (string): Type of request, in this case "video". Possible values: video and timelapse

duration (integer): Duration of the video in seconds.

format (string): Format of the video (e.g., "Road", "Driver View", etc.).

creatorType (string): The method through which the video was created (e.g., "manual", "automated", etc.).

vehicleUuid (string): Unique identifier of the vehicle associated with the video.

extraData (object): Additional data related to the video (if available).

status (string): Status of the video (e.g., "processed", "pending", etc.).

createdAt (string): Timestamp when the video was created.

updatedAt (string): Timestamp when the video was last updated.

driver (object): Information about the driver associated with the video.

driverName (string): Name of the driver.

driverId (integer): Unique identifier of the driver.

## video (object): Details about the video recording.

recordId (string): Unique identifier of the video record.

type (string): Type of video (e.g., "video", "image", etc.).

resolution (string): Resolution of the video (e.g., "640x480").

status (string): Status of the video (e.g., "processed", "pending", etc.).

url (string): URL to access the video recording.

startTime (string): Timestamp when the video recording started.

endTime (string): Timestamp when the video recording ended.

# Error Responses

In case of an error, the API will respond with an appropriate error message.

# Status Codes

200 OK : The request was successful.

401 Unauthorized : The provided User-Authentication header is invalid.

400 Bad Request : Any invalid request or param provided.

# HEADERS

User-Authentication {{auth_token}}

# GETList Videos

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/videos?page=1&perPage=10

# Overview

This API provides access to videos associated with specific vehicles.

## Query Parameters

perPage (optional): Number of videos to retrieve per page. Default is 10.

page (optional): Page number to retrieve. Default is 1.

alertId (optional): Alert Id received via Alerts Webhook

alertKind (required with alertId): Alert Kind recevied via Alerts Webhook

# Response Structure

values (array): An array of video objects.

vodId (string): Unique identifier for the video on demand (VOD).

deviceId (string): Device identifier associated with the video.

requestType (string): Type of video request.

duration (integer): Duration of the video in seconds.

format (string): Format of the video.

creatorType (string): Type of creator of the video.

vehicleUuid (string): Unique identifier of the vehicle associated with the video.

extraData (object): Additional data associated with the video.

status (string): Status of the video.

createdAt (string): Timestamp indicating when the video was created.

updatedAt (string): Timestamp indicating when the video was last updated.

driver (object): Information about the driver associated with the video.

driverName (string): Name of the driver.

driverId (integer): Unique identifier of the driver.

video (object): Information about the video itself.

recordId (string): Unique identifier for the video record.

type (string): Type of video.

resolution (string): Resolution of the video.

status (string): Status of the video.

startTime (string): Timestamp indicating the start time of the video.

endTime (string): Timestamp indicating the end time of the video.

## pagination (object): Pagination details.

page (integer): Current page number.

perPage (integer): Number of videos per page.

count (integer): Total count of videos.

more (boolean): Indicates if there are more videos available.

# Notes

Replace {vehicle_uuid} in the endpoint with the UUID of the specific vehicle you want to retrieve videos for.

Pagination parameters perPage and page can be used to navigate through the video results.

# HEADERS

Accept application/json, text/plain, */*

User-Authentication {{auth-token}}

PARAMS

requestType

creatorType manual

page 1

perPage 10

deviceId 0864281048734728

# POSTCreate Video Request

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/videos

# Overview

This API allows users to request the creation of a vehicle video. Users can specify various parameters such as format, resolution, request type, creator type, device ID, duration, and start time for the video.

# Request Body

format (string): Format of the video (e.g., "Road", "Driver", "Side-by-Side").

resolution (string): Resolution of the video (e.g., "640x480").

requestType (string): Type of video request (e.g., "video").

creatorType (string): Type of creator (e.g., "auto" or "manual").

duration (integer): Duration of the video in seconds.

startTime (integer): Start time of the video recording.

# Response Structure

vodId (string): ID of the video-on-demand (VOD).

deviceId (string): ID of the device recording the video.

requestType (string): Type of video request (e.g., "video").

duration (integer): Duration of the video in seconds.

format (string): Format of the video (e.g., "Road").

creatorType (string): Type of creator (e.g., "auto").

vehicleUuid (string): UUID of the vehicle associated with the video.

extraData (object): Additional data associated with the video.

status (string): Status of the video creation process (e.g., "pending").

createdAt (string): Timestamp of when the video was created.

updatedAt (string): Timestamp of when the video was last updated.

driver.driverName (string): Name of the driver associated with the video.

driver.driverId (integer): ID of the driver associated with the video.

video.recordId (string): ID of the recorded video.

video.type (string): Type of video (e.g., "video").

video.resolution (string): Resolution of the video (e.g., "640x480").

video.status (string): Status of the video (e.g., "pending").

startTime (string): Start time of the video recording.

endTime (string): End time of the video recording.

## HEADERS

Content-Type application/json

Accept application/json, text/plain, /

User-Authentication {{auth-token}}

Body raw


| {<br> "format": "Road",<br> "resolution": "640x480",<br> "requestType": "video",<br> "creatorType": "auto",<br> "duration": 1,<br> "startTime": 1702555021<br>} |
| --- |


## Webhooks

Webhooks are a powerful mechanism for receiving real-time notifications

about events that occur within the platform. With webhooks, you can receive instant alerts and updates directly to your application or platform, enabling you to take immediate action based on these events.

Examples of events include overspeed alerts, harsh braking alerts, and more.

## How to Consume Webhooks

1. Define Webhook Acceptor: Set up an endpoint in your application or platform to receive webhook notifications. This endpoint, known as the webhook acceptor, should be capable of handling HTTP POST requests.

2. Register Webhook Acceptor URL: Once you have defined your webhook acceptor, register its URL with us via Email. This informs our system where to send webhook notifications when relevant events occur.

3. Configure Alerts: Utilize our APIs to configure the specific alerts and events for which you want to receive webhook notifications. You can customize the types of alerts and events based on your requirements and use case.

# Webhook Alert Push

The webhook alert push feature allows users to receive real-time notifications for various events and conditions detected by the system, such as sudden braking, overspeeding, ignition status changes, and more.

By subscribing to webhooks, users can seamlessly integrate these alerts into their systems or applications, enabling proactive monitoring and response to critical vehicle-related events.

# Following are the alert supported for alert push

1. AntiTheft

2. Crash

3. CrashDuringOverspeed

4. DeviceLowBattery

5. DeviceOffline

6. DeviceRemoval

7. DriverDistracted

8. DriverMobileUse

9. Dtc

10. EntryExit

11. Fatigue

12. FuelTheft

13. Ignition

14. Movement

15. OverRev

16. Overspeed

17. Refueling

18. RouteDeviation

19. SharpTurn

20. Sos

21. Stoppage

22. SuddenAcceleration

23. SuddenBraking

24. UnwantedMovement

25. VehicleIdle

26. VehicleLowBatteryVoltage

# IMPORTANT NOTE

In the context of some alert events the webhook payload may contain both active and inactive event fields.

Understanding these fields is crucial for interpreting the start and end of an alert event. Below is a detailed explanation of this behavior:

## Active Event Fields

When an alert event begins, the webhook payload will include the following active event fields:

active_event_time: The timestamp indicating when the alert event started.

active_event_latitude: The latitude where the alert event started.

active_event_longitude: The longitude where the alert event started.

### Example:

If an ignition ON event occurs, the webhook payload will contain active event fields indicating the time and location where the ignition was turned ON.

## Inactive Event Fields

When an alert event ends, the webhook payload will include the following inactive event fields:

inactive_event_time: The timestamp indicating when the alert event ended.

inactive_event_latitude: The latitude where the alert event ended.

inactive_event_longitude: The longitude where the alert event ended.

### Example:

If an ignition OFF event occurs, the webhook payload will contain inactive event fields indicating the time and location where the ignition was turned OFF.

### POSTHarsh Braking Alert

## Overview

This Webhook provides information about a sudden braking alert event.

## Request Body

id (integer): Unique identifier in the system.

event_time (datetime): Timestamp of the event.

latitude (float): Latitude coordinate of the event location.

longitude (float): Longitude coordinate of the event location.

vehicle_number (string): Identification number of the vehicle.

created_at (datetime): Timestamp of when the event was created.

speed (float): Speed of the vehicle at the time of the event.

kind (string): Type of event, in this case, "SuddenBrakingAlert".

## Body raw (json)


| json  |
| --- |
| {<br> "id": 12345,<br> "event_time": "2024-02-08T12:30:45Z",<br> "latitude": 37.7749,<br> "longitude": -122.4194,<br> "vehicle_number": "ABC123",  |


"created_at": "2024-02-08T12:35:00Z",

"speed": 45.5,

"kind": "SuddenBrakingAlert"

}

## POSTHarsh Acceleration Alert

## Overview

This Webhook provides information about a sudden acceleration alert event.

## Request Body

id (integer): Unique identifier in the system.

event_time (datetime): Timestamp of the event.

latitude (float): Latitude coordinate of the event location.

longitude (float): Longitude coordinate of the event location.

vehicle_number (string): Identification number of the vehicle.

created_at (datetime): Timestamp of when the event was created.

speed (float): Speed of the vehicle at the time of the event.

kind (string): Type of event, in this case, "SuddenAccelerationAlert".

## Body raw (json)


| json<br>{<br> "id": 123,<br> "event_time": "2024-02-05T12:30:45Z",<br> "latitude": 37.7749,<br> "longitude": -122.4194,<br> "vehicle_number": "ABC123",<br> "created_at": "2024-02-05T12:30:45Z",<br> "speed": 65.5,<br> "kind": "SuddenAccelerationAlert"<br>} |
| --- |


## POSTOverspeed Alert

## Overview

This Webhook provides information about an overspeed alert event.

## Request Body

id (integer): Unique identifier in the system.

vehicle_number (string): Identification number of the vehicle.

event_key (string): Key associated with the event.

active_event_time (datetime): Timestamp of the active event.

active_event_latitude (float): Latitude coordinate of the active event location.

active_event_longitude (float): Longitude coordinate of the active event location.

inactive_event_time (datetime): Timestamp of the inactive event.

inactive_event_latitude (float): Latitude coordinate of the inactive event location.

inactive_event_longitude (float): Longitude coordinate of the inactive event location.

created_at (datetime): Timestamp of when the event was created.

updated_at (datetime): Timestamp of when the event was last updated.

speed (float): Speed of the vehicle at the time of the event.

kind (string): Type of event, in this case, "OverspeedAlert".

## Body raw (json)


| json<br>{<br> "id": 123,<br> "vehicle_number": "ABC123",<br> "event_key": "XYZ789",<br> "active_event_time": "2024-02-05T12:30:45Z",<br> "active_event_latitude": 37.7749,<br> "active_event_longitude": -122.4194,  |
| --- |


"inactive_event_time": "2024-02-05T12:35:45Z",

"inactive_event_latitude": 37.7749,

"inactive_event_longitude": -122.4194,

"created_at": "2024-02-05T12:30:45Z",

"updated_at": "2024-02-05T12:30:45Z",

"speed": 75.5,

"kind": "OverspeedAlert"

}

## POSTIgnition Alert

## Overview

This Webhook provides information about an ignition alert event.

# Request Body

id (integer): Unique identifier for the event.

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp of the active event.

active_event_latitude (float): Latitude coordinate of the active event location.

active_event_longitude (float): Longitude coordinate of the active event location.

inactive_event_time (datetime): Timestamp of the inactive event.

inactive_event_latitude (float): Latitude coordinate of the inactive event location.

inactive_event_longitude (float): Longitude coordinate of the inactive event location.

created_at (datetime): Timestamp of when the event was created.

event_key (string): Key associated with the event.

kind (string): Type of event, in this case, "IgnitionAlert".

## Body raw (json)


| json<br>{<br> "id": 123,<br> "vehicle_number": "ABC123",<br> "active_event_time": "2024-02-05T12:30:45Z",<br> "active_event_latitude": 37.7749,<br> "active_event_longitude": -122.4194,<br> "inactive_event_time": "2024-02-05T12:35:45Z",<br> "inactive_event_latitude": 37.7749,<br> "inactive_event_longitude": -122.4194,<br> "created_at": "2024-02-05T12:30:45Z",<br> "event_key": "XYZ789",<br> "kind": "IgnitionAlert"<br>} |
| --- |


## POSTIdling Alert

# Overview

This Webhook provides information about an idling alert event.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp when idling alert conditions are met.

active_event_latitude (float): Latitude coordinate of the vehicle when idling alert is active.

active_event_longitude (float): Longitude coordinate of the vehicle when idling alert is active.

inactive_event_time (datetime): Timestamp when idling alert becomes inactive.

inactive_event_latitude (float): Latitude coordinate of the vehicle when idling alert is inactive.

inactive_event_longitude (float): Longitude coordinate of the vehicle when idling alert is inactive.

created_at (datetime): Timestamp of when the alert was created.

kind (string): Type of event, in this case, "IdlingAlert".

## Body raw (json)

json

{

"id": 123,

"vehicle_number": "ABC123",

"active_event_time": "2024-02-05T12:30:45Z",

"active_event_latitude": 37.7749,

"active_event_longitude": -122.4194,

"inactive_event_time": "2024-02-05T12:35:45Z",

"inactive_event_latitude": 37.7749,

"inactive_event_longitude": -122.4194,

"created_at": "2024-02-05T12:30:45Z",

"kind": "IdlingAlert"

}

# POSTFatigue Alert

# Overview

This Webhook provides information about a fatigue alert event.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

start_time (datetime): Timestamp indicating when fatigue alert calculation started, also known as Ignition on time.

active_event_time (datetime): Timestamp when fatigue alert conditions are met.

inactive_event_time (datetime): Timestamp when the driver stops after completing the trip duration, also known as Ignition off time.

active_event_latitude (float): Latitude coordinate of the vehicle when fatigue alert is active.

active_event_longitude (float): Longitude coordinate of the vehicle when fatigue alert is active.

inactive_event_latitude (float): Latitude coordinate of the vehicle when fatigue alert is inactive.

inactive_event_longitude (float): Longitude coordinate of the vehicle when fatigue alert is inactive.

kind (string): Type of event, in this case, "FatigueAlert".

# Body raw (json)


| json<br>{<br> "id": 123,<br> "vehicle_number": "ABC123",<br> "start_time": "2024-02-05T12:30:45Z",<br> "active_event_time": "2024-02-05T12:35:45Z",<br> "inactive_event_time": "2024-02-05T13:30:45Z",<br> "active_event_latitude": 37.7749,<br> "active_event_longitude": -122.4194,<br> "inactive_event_latitude": 37.7749,<br> "inactive_event_longitude": -122.4194,<br> "kind": "FatigueAlert"<br>} |
| --- |


# POSTOverrev(RPM) Alert

# Overview

This Webhook provides information about an overrev alert event when a vehicle's engine exceeds its maximum recommended revolutions per minute (RPM).

Over-revving occurs when the engine is pushed beyond its safe operating

limits, which can lead to mechanical stress, excessive wear and tear,

and potential damage to the engine components.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

event_key (string): Key associated with the event.

rpm_value (integer): RPM (Revolutions Per Minute) value triggering the overrev alert.

start_time (datetime): Timestamp indicating when the overrev alert condition started.

active_event_time (datetime): Timestamp when the overrev alert condition was active.

inactive_event_time (datetime): Timestamp of the inactive event.

inactive_event_latitude (float): Latitude coordinate of the inactive event location.

inactive_event_longitude (float): Longitude coordinate of the inactive event location.

created_at (datetime): Timestamp indicating when the alert was created.

kind (string): Type of event, in this case, "OverrevAlert".

# Body raw (json)

json

{

"id": 456,

"vehicle_number": "XYZ789",

"event_key": "abc123",

"rpm_value": 6000,

"start_time": "2024-02-05T10:15:30Z",

"active_event_time": "2024-02-05T10:20:30Z",

"active_event_latitude": 37.7749,

"active_event_longitude": -122.4194,

"inactive_event_time": "2024-02-05T12:35:45Z",

"inactive_event_latitude": 37.7749,

"inactive_event_longitude": -122.4194,

"created_at": "2024-02-05T10:30:30Z",

"kind": "OverrevAlert"

}

# POSTAnti Theft Alert

# Overview

This Webhook provides information about an anti-theft alert event.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

event_time (datetime): Timestamp indicating when the anti-theft alert occurred.

latitude (float): Latitude coordinate of the vehicle at the time of the alert.

longitude (float): Longitude coordinate of the vehicle at the time of the alert.

created_at (datetime): Timestamp indicating when the alert record was created.

kind (string): Type of event, in this case, "AntiTheftAlert".

# Body raw (json)


| json<br>{<br> "id": 123,<br> "vehicle_number": "ABC123",<br> "event_time": "2024-02-05T10:30:45Z",<br> "latitude": 40.7128,<br> "longitude": -74.0060,<br> "created_at": "2024-02-05T10:35:12Z",<br> "kind": "AntiTheftAlert"<br>} |
| --- |


# POSTGeofence Alert

# Overview

This Webhook provides information about a geofence alert event.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

polygon_id (integer): ID of the geofence polygon associated with the alert.

event_key (string): Key indicating the type of geofence event (e.g., "geofence_enter", "geofence_exit").

active_event_time (datetime): Timestamp indicating when the vehicle entered or exited the geofence.

active_event_latitude (float): Latitude coordinate of the vehicle when the geofence event occurred.

active_event_longitude (float): Longitude coordinate of the vehicle when the geofence event occurred.

inactive_event_time (datetime): Timestamp indicating when the geofence event became inactive.

inactive_event_latitude (float): Latitude coordinate of the vehicle when the geofence event became inactive.

inactive_event_longitude (float): Longitude coordinate of the vehicle when the geofence event became inactive.

created_at (datetime): Timestamp indicating when the alert record was created.

kind (string): Type of event, in this case, "GeofenceAlert".

Body raw (json)


| json<br>{<br> "id": 123,<br> "vehicle_number": "ABC123",<br> "polygon_id": 456,<br> "event_key": "geofence_enter",<br> "active_event_time": "2024-02-05T10:30:45Z",<br> "active_event_latitude": 40.7128,<br> "active_event_longitude": -74.0060,<br> "inactive_event_time": "2024-02-05T10:45:00Z",<br> "inactive_event_latitude": 40.7129,<br> "inactive_event_longitude": -74.0061,<br> "created_at": "2024-02-05T10:35:12Z",<br> "kind": "GeofenceAlert"<br>} |
| --- |


# POSTCrash detection with speed limit

# Overview

This Webhook provides information about an alert indicating a crash during an overspeed event.

# Request Body

id (integer): Unique identifier for the alert.

event_time (datetime): Timestamp indicating when the crash occurred.

latitude (float): Latitude coordinate of the vehicle at the time of the crash.

longitude (float): Longitude coordinate of the vehicle at the time of the crash.

speed (float): Speed of the vehicle at the time of the crash.

vehicle_number (string): Identification number of the vehicle.

created_at (datetime): Timestamp indicating when the alert record was created.

updated_at (datetime): Timestamp indicating when the alert record was last updated.

kind (string): Type of event, in this case, "CrashDuringOverspeedAlert".

# Body raw (json)


| json<br>{<br> "id": 7,<br> "event_time": "2022-08-09T14:47:44.000+05:30",<br> "latitude": 22.44372,<br> "longitude": 73.33989,<br> "speed": 25.0,<br> "vehicle_number": "508",<br> "created_at": "2022-08-09T14:47:46.866+05:30",<br> "updated_at": "2022-08-09T14:47:46.866+05:30",<br> "kind": "CrashDuringOverspeedAlert"<br>} |
| --- |


# POSTDevice Removal Alert

# Overview

This Webhook provides information about an alert indicating the removal of a device from a vehicle.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp indicating when the device removal event was activated.

active_event_latitude (float): Latitude coordinate of the vehicle when the device removal event was activated.

active_event_longitude (float): Longitude coordinate of the vehicle when the device removal event was activated.

inactive_event_time (datetime): Timestamp indicating when the device removal event was deactivated.

inactive_event_latitude (float): Latitude coordinate of the vehicle when the device removal event was deactivated.

inactive_event_longitude (float): Longitude coordinate of the vehicle when the device removal event was deactivated.

created_at (datetime): Timestamp indicating when the alert record was created.

event_key (string): Key associated with the event.

kind (string): Type of event, in this case, "DeviceRemovalAlert".

## Body raw (json)

json

{

"id": 123,

"vehicle_number": "ABC123",

"active_event_time": "2024-02-10T08:30:00",

"active_event_latitude": 37.7749,

"active_event_longitude": -122.4194,

"inactive_event_time": "2024-02-10T08:35:00",

"inactive_event_latitude": 37.7749,

"inactive_event_longitude": -122.4194,

"created_at": "2024-02-10T08:40:00",

"event_key": "12345",

"kind": "DeviceRemovalAlert"

}

## POSTVehicle Low Battery Voltage Alert

## Overview

This Webhook provides information about an alert indicating low battery voltage in a vehicle.

# Request Body

id (integer): Unique identifier for the alert.

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp indicating when the low battery voltage alert was activated.

active_event_latitude (float): Latitude coordinate of the vehicle when the low battery voltage alert was activated.

active_event_longitude (float): Longitude coordinate of the vehicle when the low battery voltage alert was activated.

inactive_event_time (datetime): Timestamp indicating when the low battery voltage alert was deactivated.

inactive_event_latitude (float): Latitude coordinate of the vehicle when the low battery voltage alert was deactivated.

inactive_event_longitude (float): Longitude coordinate of the vehicle when the low battery voltage alert was deactivated.

created_at (datetime): Timestamp indicating when the alert record was created.

event_key (string): Key associated with the event.

kind (string): Type of event, in this case, "VehicleLowBatteryVoltageAlert".

# Body raw (json)

json

{

"id": 789,

"vehicle_number": "XYZ456",

"active_event_time": "2024-02-10T10:15:00",

"active_event_latitude": 40.7128,

"active_event_longitude": -74.006,

"inactive_event_time": "2024-02-10T10:20:00",

"inactive_event_latitude": 40.7128,

"inactive_event_longitude": -74.006,

"created_at": "2024-02-10T10:25:00",

"event_key": "78901",

"kind": "VehicleLowBatteryVoltageAlert"

}

<!-- POSTSharp turn Alert -->

Sharp Turn

# Overview

This Webhook provides information about a sharp turn alert detected in a vehicle.

# Request Body

id (integer): Unique identifier for the sharp turn alert.

event_time (datetime): Timestamp indicating when the sharp turn alert occurred.

latitude (float): Latitude coordinate of the vehicle when the sharp turn alert occurred.

longitude (float): Longitude coordinate of the vehicle when the sharp turn alert occurred.

truck_id (integer): ID of the truck associated with the sharp turn alert.

vehicle_number (string): Identification number of the vehicle.

created_at (datetime): Timestamp indicating when the sharp turn alert record was created.

updated_at (datetime): Timestamp indicating when the sharp turn alert record was last updated.

speed (float): Speed of the vehicle at the time of the sharp turn alert.

kind (string): Type of event, in this case, "SharpTurnAlert".

# Body raw (json)


| json<br>{<br> "id": 123,<br> "event_time": "2024-02-10T14:30:00",<br> "latitude": 40.7128,<br> "longitude": -74.006,<br> "truck_id": 456,<br> "vehicle_number": "ABC123",<br> "created_at": "2024-02-10T14:35:00",<br> "updated_at": "2024-02-10T14:35:00",<br> "speed": 30.5,<br> "kind": "SharpTurnAlert"<br>} |
| --- |


# POSTDtc Alert

# Overview

This Webhook provides information about a Diagnostic Trouble Code (DTC) alert detected in a vehicle when it detects a fault or issue within the vehicle's components or systems.

These alerts are generated based on specific error codes stored in the vehicle's computer system, indicating problems such as engine malfunctions, emission control system issues, transmission problems, or other mechanical or electrical faults.

# Request Body

id (integer): Unique identifier for the DTC alert.

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp indicating when the DTC alert became active.

active_event_latitude (float): Latitude coordinate of the vehicle when the DTC alert became active.

active_event_longitude (float): Longitude coordinate of the vehicle when the DTC alert became active.

inactive_event_time (datetime): Timestamp indicating when the DTC alert became inactive.

inactive_event_latitude (float): Latitude coordinate of the vehicle when the DTC alert became inactive.

inactive_event_longitude (float): Longitude coordinate of the vehicle when the DTC alert became inactive.

created_at (datetime): Timestamp indicating when the DTC alert record was created.

event_key (string): Key identifying the DTC event.

dtc_code (string): Diagnostic Trouble Code associated with the alert.

kind (string): Type of event, in this case, "DtcAlert".

## Body raw (json)

json

{

"id": 123,

"vehicle_number": "ABC123",

"active_event_time": "2024-02-10T14:30:00",

"active_event_latitude": 40.7128,

"active_event_longitude": -74.006,

"inactive_event_time": "2024-02-10T14:35:00",

"inactive_event_latitude": 40.7129,

"inactive_event_longitude": -74.007,

"created_at": "2024-02-10T14:35:00",

"event_key": "DTCA123",

"dtc_code": "P0123",

"kind": "DtcAlert"

}

## POSTRefueling Alert

# Overview

This Webhook provides information about a refueling event detected by the system.

# Request Body

id (integer): Unique identifier for the refueling event.

kind (string): Type of event, in this case, "RefuelingAlert".

vehicle_number (string): Identification number of the vehicle.

event_time (datetime): Timestamp indicating when the refueling event occurred.

latitude (float): Latitude coordinate of the vehicle when the refueling event occurred.

longitude (float): Longitude coordinate of the vehicle when the refueling event occurred.

refueled_in_percent (float): Percentage of fuel tank refilled during the event.

refueled_in_liters (float): Volume of fuel refilled in liters during the event.

created_at (datetime): Timestamp indicating when the refueling event record was created.

updated_at (datetime): Timestamp indicating when the refueling event record was last updated.

fuel_tank_uuid (string): UUID of the fuel tank associated with the refueling event.

# Body raw (json)

json

{

"id": 123,

"kind": "RefuelingAlert",

"vehicle_number": "ABC123",

"event_time": "2024-02-10T15:00:00",

"latitude": 40.7128,

"longitude": -74.006,

"refueled_in_percent": 75.0,

"refueled_in_liters": 30.0,

"created_at": "2024-02-10T15:01:00",

"updated_at": "2024-02-10T15:01:00",

"fuel_tank_uuid": "abc-123-def"

}

# POSTFuelTheft Alert

# Overview

This Webhook provides information about a possible fuel theft alert detected by the system.

# Request Body

id (integer): Unique identifier for the possible fuel theft alert.

kind (string): Type of event, in this case, "PossibleFuelTheftAlert".

vehicle_number (string): Identification number of the vehicle.

event_time (datetime): Timestamp indicating when the possible fuel theft alert occurred.

latitude (float): Latitude coordinate of the vehicle when the alert occurred.

longitude (float): Longitude coordinate of the vehicle when the alert occurred.

fuel_theft_in_percent (float): Estimated percentage of fuel lost due to possible theft.

fuel_theft_in_liters (float): Estimated volume of fuel lost in liters due to possible theft.

created_at (datetime): Timestamp indicating when the alert record was created.

updated_at (datetime): Timestamp indicating when the alert record was last updated.

fuel_tank_uuid (string): UUID of the fuel tank associated with the possible fuel theft alert.
<!-- Body raw (json) -->


| json<br>{<br> "id": 456,<br> "kind": "PossibleFuelTheftAlert",<br> "vehicle_number": "XYZ789",<br> "event_time": "2024-02-10T16:30:00",<br> "latitude": 34.0522,<br> "longitude": -118.2437,<br> "fuel_theft_in_percent": 20.0,<br> "fuel_theft_in_liters": 10.0,<br> "created_at": "2024-02-10T16:31:00",<br> "updated_at": "2024-02-10T16:31:00",<br> "fuel_tank_uuid": "xyz-789-abc"<br>} |
| --- |


# POSTDeviceOffline Alert

# Overview

This Webhook provides information about a device offline alert detected by the system.

# Request Body

id (integer): Unique identifier for the device offline alert.

kind (string): Type of event, in this case, "DeviceOfflineAlert".

vehicle_number (string): Identification number of the vehicle.

active_event_time (datetime): Timestamp indicating when the device went offline.

active_event_latitude (float): Latitude coordinate of the vehicle when the device went offline.

active_event_longitude (float): Longitude coordinate of the vehicle when the device went offline.

inactive_event_time (datetime): Timestamp indicating when the device came back online.

inactive_event_latitude (float): Latitude coordinate of the vehicle when the device came back online.

inactive_event_longitude (float): Longitude coordinate of the vehicle when the device came back online.

created_at (datetime): Timestamp indicating when the alert record was created.

updated_at (datetime): Timestamp indicating when the alert record was last updated.

# Body raw (json)

json

{

"id": 123,

"kind": "DeviceOfflineAlert",

"vehicle_number": "ABC123",

"active_event_time": "2024-02-10T10:00:00",

"active_event_latitude": 40.7128,

"active_event_longitude": -74.0060,

"inactive_event_time": "2024-02-10T10:30:00",

"inactive_event_latitude": 40.7128,

"inactive_event_longitude": -74.0060,

"created_at": "2024-02-10T10:35:00",

"updated_at": "2024-02-10T10:35:00"

}

# Webhook Live Location Push

This webhook offers real-time vehicle location push via webhook integration. This feature allows customers to receive live updates of their vehicle's location directly into their system. The raw data provided includes essential parameters such as speed, GPS time, ignition status, latitude,longitude, and driving behavior indicators like sharp turns, harsh braking, and harsh acceleration.

# Requirements

Customers need to provide an API endpoint to receive live location data.

The request body structure of the customer's API should be compatible with the format of the data pushed by Loconav.

IP/domain whitelisting should be configured on the customer's end. Loconav provides the domain for whitelisting purposes.

## Usage of the Data:

Customers can parse and store the live location data received from Loconav.

The raw data can be utilized for various purposes such as displaying live vehicle location on maps, providing speed and time information to customers, and performing further analysis.

Fields such as sharp turns, harsh braking, and harsh acceleration can be leveraged for generating alerts and calculating metrics like driver or vehicle scores.

## Common Use Cases:

1. Live Location Display: Customers can visualize the live location of their vehicles on maps in real time.

2. Speed and Time Information: Speed and time data can be presented to customers for better monitoring and management.

3. Driving Behavior Analysis: The provided driving behavior indicators can be used to analyze driver behavior and vehicle performance.

4. Alert Generation: Events such as sharp turns, harsh braking, and harsh acceleration can trigger alerts for immediate action.

## POSTVehicle Live Location Push

Overview:

The Live Location GPS Push webhook delivers real-time updates of a vehicle's GPS information, including its current speed, GPS time, ignition status, latitude, longitude, orientation, and various driving behaviors such as sharp turns,harsh braking, and harsh acceleration.

### Request Body:

imei : IMEI number of the device.

speed : (kmph)Current speed of the vehicle.

gpstime : GPS time indicating the timestamp of the location data.

ignition : Ignition status of the vehicle (1 for on, 0 for off).

latitude : Latitude coordinate of the vehicle's current location.

longitude : Longitude coordinate of the vehicle's current location.

sharpTurn : Indicator for sharp turn events (1 for detected, 0 for not detected).

orientation : Orientation of the vehicle. (refers to the direction in which the vehicle is facing, often measured in degrees relative to the North direction)

harshBraking : Indicator for harsh braking events (1 for detected, 0 for not detected).

vehiclenumber : Vehicle registration number.

rockBreakerPedal : Indicator for rock breaker pedal status (1 for engaged, 0 for disengaged).

harshAcceleration : Indicator for harsh acceleration events (1 for detected, 0 for not detected).

## Body raw (json)

json

{

"imei": "0210716299",

"speed": 0.0,

"gpstime": "17-12-2021 09:57:07",

"ignition": "1",

"latitude": 11.125757,

"longitude": 79.140228,

"sharpTurn": "0",

"orientation": 201.0,

"harshBraking": "0",

"vehiclenumber": "TN19AA7420",

"rockBreakerPedal": "0",

"harshAcceleration": "0"

}

# Alert Subscriptions

With our Alert subscription APIs, you can manage the alerts effectively on a platform

# GETGet alert subscription

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicle_uuid}}/alerts/subscriptions

# Get Vehicle Alerts Subscriptions

This endpoint retrieves the alert subscriptions for a specific vehicle.

# Request

Method: GET

URL:

https://app.a.loconav.com/integration/api/v1/vehicles/{{vehicle_uuid}}/alerts/subscrip tions

# HEADERS

User-Authentication {{token}}

# POSTCreate Alert Subscriptions

https://api.a.loconav.com/integration/api/v1/vehicles/alerts/subscriptions

Each kind of alert will have different fields for alert_config, specific config is below :

“vehicle_numbers” : [], // array of vehicle number, wether this or id only one is processed, id first priority

in all kind either use vehicle id or number whichever applicable.

# Overspeed

“kind”: “overspeed”,

“vehicleIds” : [], // array of vehicle ids

“includeAll” : “0”,

“alertConfig”:{

“speedLimit”: “200”,

“minDurationInMinutes”: “100”,

“minDurationInSeconds”: “10”

}

Entry_exit

kind”: “entry_exit”,

“vehicleIds” : [], // array of vehicle ids

“includeAll” : “0”,

“alertConfig”:{

“polygonIds”: [],

“includeAllPolygons”: 0/1

}

Sudden Braking

“kind”: “sudden_braking”,

“vehicleIds” : [], // array of vehicle ids

“includeAll” : “0”,

Sudden acceleration

“kind”: “sudden_acceleration”,

“vehicleIds” : [], // array of vehicle ids

“includeAll” : “0”,

Vehicle Idling Alert

“Kind” : “vehicle_idle”,

“vehicleIds” : [],

“includeAll” : “0”,

“alertConfig” : {

“minDuration” : “10”

}

Fatigue Alert

“kind” : “fatigue”,

"vehicleIds" : [],

"includeAll" : "0",

“alertConfig” : {

“fatigueDurationInMinutes” : “100”,

“stoppageTimeToIgnoreInMinutes” : “15”

}

Antitheft Alert

“kind” : “anti_theft”,

"vehicleIds" : ["2"],

"includeAll" : "0",

“alertConfig” : {

“startTime” : “15:35”,

“endTime” : “15:45”

}

Over rev Alert

“kind” : “over_rev”,

"vehicleIds" : [],

"includeAll" : "0",

“alertConfig” : {

“rpmValue” : “40”,

“minDurationInMinutes”: “100”,

“minDurationInSeconds”: “10”

}

TowAway Alert

“kind” : “tow_away”,

"vehicleIds" : []

}

vehicle low battery

“kind” : “vehicle_low_battery_voltage”,

"vehicleIds" : [],

"includeAll" : "0",

“alertConfig” : {

"batteryVoltage": "X"

}

device removal

“kind” : “device_removal”,

"vehicleIds" : ["2"],

"includeAll" : "0"

crash detection

“kind” : “crash_during_overspeed”,

"vehicleIds" : ["2"],

"includeAll" : "0",

“alertConfig” : {

"speedLimit": "X"

}

Sharp Turn Braking

“kind”: “sharp_turn”,

“vehicleIds” : [], // array of vehicle ids

“includeAll” : “0”,

“alertConfig” : {

"speedLimit": "X"

}

HEADERS

User-Authentication {{token}}

Content-Type application/json

Body raw (json)

json

{

"alertSubscriptions": [

{

"kind": "overspeed",

"vehicleIds": [

"67fd83f8-d9d2-438d-872c-586299aedc0f"

],

"includeAll": "0"

 }

],

"alertConfig": {

"speedLimit": "200",

"minDurationInMinutes": "100",

"minDurationInSeconds": "10"

 }

 }

# PUTUpdate Alert Subscription

<!-- https://api.a.loconav.com/integration/api/v1/vehicles/alerts/subscriptions -->

# Update Vehicle Alert Subscriptions

This endpoint allows the user to update the alert subscriptions for vehicles.

# Request Body

alertSubscriptions (array of objects) - An array containing the details of alert subscriptions.

id (number) - The ID of the alert subscription.

kind (string) - The type of alert subscription.

vehicleIds (array of strings) - An array of vehicle IDs for which the alert subscription is being updated.

alertConfig (object) - The configuration for the alert subscription.

minDurationInMinutes (number) - The minimum duration in minutes for the alert.

minDurationInSeconds (number) - The minimum duration in seconds for the alert.

speedLimit (number) - The speed limit for the alert.

subUserIds (array of numbers) - An array of user IDs for the alert subscription.

vehicleGroupIds (array of numbers) - An array of vehicle group IDs for the alert subscription.

# Response

status (boolean) - Indicates the status of the request. true for success.

data (string) - Additional data related to the request.

## Example Response:


| json<br>{<br> "status": true,<br> "data": ""<br>} |
| --- |


## HEADERS

Content-Type application/json

User-Authentication {{token}}

Body raw (json)


| json  |  |
| --- | --- |
| {<br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br>  |  "alertSubscriptions": [<br> {<br> "id": 2313,<br> "kind": "overspeed",<br> "vehicleIds": [<br> "e7eb2c16-c6d9-49ac-a1f1-7bf45a31c38c"<br> ],<br> "alertConfig": {<br> "minDurationInMinutes": 1,<br> "minDurationInSeconds": 2,<br> "speedLimit": 6,<br> "subUserIds": [<br> 5521,<br> 4780,<br> 6063,<br> 6064<br> ],<br> "vehicleGroupIds": [<br> 3621<br> ]<br> }<br> }<br> ]<br> } |


DELETEDelete Alert Subscription

https:://app.a.loconav.com/integration/api/v1/vehicles/alerts/subscriptions/374

# Delete Vehicle Alert Subscription

This endpoint is used to delete a specific vehicle alert subscription by providing the subscription ID in the URL.

# Response

The response for this request is a JSON object with the following schema:

The status property indicates the success or failure of the request, where true denotes success. The data property may contain additional information related to the deletion operation.

# HEADERS

User-Authentication {{token}}

PARAMS

# Mobilization

POSTCreate Vehicle Mobilization Request

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/immobilizer_requests

# Overview

The Immobilizer Requests API allows users to send requests to immobilize or mobilize a specific vehicle. This can be useful for security and safety purposes, enabling the control of a vehicle's movement remotely.

This is a async operation and will take some time. Call Get Mobilization requests API to know the status

# Path Parameters

vehicleId (string, required): The unique identifier of the vehicle for which the immobilizer request is made.

# Request Body

value (string, required): The action to be performed on the immobilizer. Possible values are "MOBILIZE" or "IMMOBILIZE".

# Response Body

id (integer): The unique identifier of the immobilizer request. Customers can use this Id and call Get Mobilization request to find the status of the operation

# Status Codes

200 OK : The request was successful, and the immobilizer request was processed.

400 Bad Request : The request body contains invalid data.

422 Unprocessable Entity : The specified vehicle is not set up for immobilization.

# HEADERS

User-Authentication {{auth-token}}

Body raw (json)


| json<br>{<br> "value":"MOBILIZE"<br>} |
| --- |


# GETGet Mobilization Requests

https://api.a.loconav.com/integration/api/v1/vehicles/immobilization_requests/{{immobilizationRequestId}}

Overview

The Immobilization Request Details API allows users to retrieve details about a specific immobilization request made for a vehicle. This includes information such as the status of the request, the reason for immobilization, and the user who initiated the request.

# Request Headers

User-Authentication : The authentication token for accessing the API. Replace {{auth-token}} with the actual authentication token.

# Path Parameters

immobilizationRequestId (string, required): The unique identifier of the immobilization request for which details are requested.

# Response Body

id (integer): The unique identifier of the immobilization request.

truck_id (integer): The identifier of the truck associated with the request.

status (string): The status of the immobilization request (e.g., "success", "pending", "failed").

message (string): A message indicating the result of the immobilization request.

mobilize (boolean): Indicates whether the request was for mobilization ( true ) or immobilization ( false ).

created_via (string): The method or platform through which the request was created.

created_at (integer): The timestamp when the request was created.

updated_at (integer): The timestamp when the request was last updated.

creator_type (string): The type of user who initiated the request (e.g., "User", "Admin").

creator_email (string): The email address of the user who initiated the request.

reason (string): The reason provided for the immobilization request (if applicable).

# Status Codes

200 OK : The request was successful, and the details of the immobilization request are provided.

404 Not Found : The requested immobilization request was not found.

422 Unprocessable Entity : The associated truck is not set up for immobilization.

# HEADERS

User-Authentication {{auth-token}}

# Vehicles

Loconav's Vehicle APIs offer developers a powerful toolkit for real-time fleet management. The Fetch Vehicle Details API provides comprehensive vehicle insights, while the Last Known Stats API delivers live statistics.

These APIs enable developers to create efficient, data-driven solutions for fleet monitoring and analytics, enhancing operational efficiency and decision-making.

# Telematics

Thes APIs allows you to access telematics data for vehicles, enabling you to retrieve real-time information and history about their status, location, and various sensor readings.

# POSTLast known

https://api.a.loconav.com/integration/api/v1/vehicles/telematics/last_known?page=1&perPage=10

# Overview

The Vehicle Last Known Status API allows users to retrieve the latest telemetry data for one or more vehicles,including information such as GPS coordinates, vehicle speed, ignition status, vehicle battery level and more.

# Request Parameters

vehicleIds (array, optional): An array of vehicle UUIDs for which the last known status is requested. If not provided, telemetry data for all vehicles is returned.

sensors (array): An array specifying the sensors for which data is requested. Currently, only up to 3 sensors can be specified at a time.

# Response Structure

values (array): Array containing telemetry data for each requested vehicle.

vehicleNumber (string): Vehicle registration number.

vehicleId (string): Unique identifier for the vehicle.

sensors (object): Telemetry data for the requested sensors.

pagination (object): Pagination details.

page (integer): Current page number.

perPage (integer): Number of vehicles per page.

count (integer): Total count of vehicles in the response.

more (boolean): Indicates whether there are more pages of data available.

# Note

If the vehicleIds parameter is not provided, telemetry data for all vehicles will be returned in a paginated form.

Only up to 3 sensors can be specified at a time in the sensors array.

If sensors are not passed, GPS sensors are returned by default

GPS object is a special object which contains speed, ignition, orientation, currentLocationCoordinates

axleLoad1 - axleLoad5 count as a single type against the limit of 3. For example, you could list types=gps,batteryTemperature,axleLoad1,axleLoad4 because axleLoad1 and axleLoad4 count as a single stat type. axleLoad1 and axleLoad4 still count as their own individual types.

## Supported sensors

More than 50+ sensors are supported. Below are the list of supported sensors

absoluteFuelRailPressure absoluteLoadValue ac accelerationPedalPosition

acceleratorPedalPosition1 acceleratorPedalPosition adbluLevel altitude

ambientAirTemperature ambientPressure appVersion autoRetarderSwitch axleLoad1

axleLoad2 axleLoad3 axleLoad4 axleLoad5 axleWeight backCapLock barometricPressure

batteryChargeState batteryLevel batteryTemperature bleBattery bleHumidity

bluetoothBattery1 bluetoothHumidity1 bluetoothHumidity2 bluetoothHumidity3

bluetoothHumidity4 bmsBatteryCurrent bmsBatteryStrings bmsBatteryVoltage

bmsCellOverTemperature bmsCellOverVoltage bmsCellTemperature10 bmsCellTemperature11

bmsCellTemperature12 bmsCellTemperature13 bmsCellTemperature14 bmsCellTemperature15

bmsCellTemperature16 bmsCellTemperature1 bmsCellTemperature2 bmsCellTemperature3

bmsCellTemperature4 bmsCellTemperature5 bmsCellTemperature6 bmsCellTemperature7

bmsCellTemperature8 bmsCellTemperature9 bmsCellTemperature bmsCellUnderTemperature

bmsCellUnderVoltage bmsCellVoltage10 bmsCellVoltage11 bmsCellVoltage12 bmsCellVoltage13

bmsCellVoltage14 bmsCellVoltage15 bmsCellVoltage16 bmsCellVoltage17 bmsCellVoltage18

bmsCellVoltage19 bmsCellVoltage1 bmsCellVoltage20 bmsCellVoltage21 bmsCellVoltage22

bmsCellVoltage23 bmsCellVoltage24 bmsCellVoltage25 bmsCellVoltage26 bmsCellVoltage27

bmsCellVoltage28 bmsCellVoltage29 bmsCellVoltage2 bmsCellVoltage30 bmsCellVoltage3

bmsCellVoltage4 bmsCellVoltage5 bmsCellVoltage6 bmsCellVoltage7 bmsCellVoltage8

bmsCellVoltage9 bmsCellVoltage bmsCellVoltHighLevel1 bmsCellVoltHighLevel2

bmsCellVoltHighLevel bmsCellVoltLowLevel1 bmsCellVoltLowLevel2 bmsCellVoltLowLevel

bmsChargeCapacity bmsChargeCycleNumber bmsChargeDischargeCycles

bmsChargeDischargeStatus bmsChargeOverCurrent bmsChargerStatus bmsCharging

bmsChargingCurrent bmsChargingMosSwitchControl bmsChargingMosTubeStatus

bmsChargingSwitchControlReverseCode bmsChgOvercurrentLevel1 bmsChgOvercurrentLevel2

bmsChgOvercurrentLevel bmsChgTempHighLevel1 bmsChgTempHighLevel2 bmsChgTempHighLevel

bmsChgTempLowLevel1 bmsChgTempLowLevel2 bmsChgTempLowLevel bmsCurrent bmsDiffTempLevel1

bmsDiffTempLevel2 bmsDiffTempLevel bmsDiffVoltLevel1 bmsDiffVoltLevel2 bmsDiffVoltLevel

bmsDischargeCycles bmsDischargeMosSwitchControl bmsDischargeOverCurrent

bmsDischargeSwitchControlBackcode bmsDischargingCurrent bmsDischargingMosTubeStatus

bmsDischgOvercurrentLevel1 bmsDischgOvercurrentLevel2 bmsDischgOvercurrentLevel

bmsDischgTempHighLevel1 bmsDischgTempHighLevel2 bmsDischgTempHighLevel

bmsDischgTempLowLevel1 bmsDischgTempLowLevel2 bmsDischgTempLowLevel

bmsDistanceTravelledAll bmsDistanceTravelledToday bmsEquilibriumState10

bmsEquilibriumState11 bmsEquilibriumState12 bmsEquilibriumState13 bmsEquilibriumState14

bmsEquilibriumState15 bmsEquilibriumState16 bmsEquilibriumState1 bmsEquilibriumState2

bmsEquilibriumState3 bmsEquilibriumState4 bmsEquilibriumState5 bmsEquilibriumState6

bmsEquilibriumState7 bmsEquilibriumState8 bmsEquilibriumState9 bmsEquilibriumState

bmsEquilibriumStatus17 bmsEquilibriumStatus18 bmsEquilibriumStatus19

bmsEquilibriumStatus20 bmsEquilibriumStatus21 bmsEquilibriumStatus22

bmsEquilibriumStatus23 bmsEquilibriumStatus24 bmsEquilibriumStatus25

bmsEquilibriumStatus26 bmsEquilibriumStatus27 bmsEquilibriumStatus28

bmsEquilibriumStatus29 bmsEquilibriumStatus30 bmsEquilibriumStatus31

bmsEquilibriumStatus32 bmsEquilibriumStatus bmsFullCapacity bmsLife bmsLoadStatus

bmsMaximumCellTemperatureNumber bmsMaximumCellTemperatureValue

bmsMaximumCellVoltageNumber bmsMaximumCellVoltageValue bmsMinimumCellTemperatureNumber

bmsMinimumCellTemperatureValue bmsMinimumCellVoltageNumber bmsMinimumCellVoltageValue

bmsNtcProbes bmsNtcTemperature1 bmsNtcTemperature2 bmsNtcTemperature3

bmsNtcTemperature4 bmsNtcTemperature5 bmsNtcTemperature6 bmsNtcTemperature

bmsNumberOfBatteryString bmsNumberOfTemperature bmsProductionDate bmsProtectionMarks

bmsResidualCapacity bmsShortCircuit bmsSoc bmsSocHighLevel1 bmsSocHighLevel2

bmsSocHighLevel bmsSocLowLevel1 bmsSocLowLevel2 bmsSocLowLevel bmsSoftwareVersion

bmsStatusSymbol bmsSumVoltHighLevel1 bmsSumVoltHighLevel2 bmsSumVoltHighLevel

bmsSumVoltLowLevel1 bmsSumVoltLowLevel2 bmsSumVoltLowLevel bmsSystemError

bmsTemperatureFrameNumber1 bmsTemperatureFrameNumber bmsTerminalVoltage bmsVoltage

bmsVoltageFrameNumber1 bmsVoltageFrameNumber2 bmsVoltageFrameNumber3

bmsVoltageFrameNumber4 bmsVoltageFrameNumber5 bmsVoltageFrameNumber6

bmsVoltageFrameNumber boostPressure brakePedalSwitch calculatedEngineLoadValue

canOdometerValue canSpeed cellId chargedAirCoolerTemp clutchPedal compressor

controlModuleVoltage controlStateFlag controlStateFlagP4 cruiseControl

currentLocationValue dataDownloadSizeInKb dataUploadSizeInKb

desiredPol1InjectionQuantity1 desiredPol1InjectionQuantity2 desiredPol1InjectionQuantity

desiredPol2InjectionQuantity1 desiredPol2InjectionQuantity2 desiredPol2InjectionQuantity

deviceBattery deviceBatteryLevel deviceFirmwareVersion deviceTemperature digitalInput1

digitalInput2 digitalInput3 digitalInput4 digitalOutput1 directFuelRailPressure

distanceMilOn distanceToEmptyKm distanceTravelledSinceCodeCleared door driverDoor

driverPropulsionTorque driverSeatBelt drum egrPosition egrPosSensorVoltage elock

engineCoolantTemperature engineFuelRate engineFuelTemperature engineHours

engineIntakeManifold1Temperature engineIntakeManifoldTemperature engineOilLevel

engineOilPressure engineOilPressureInMv engineOilTemperature engineOilTemperatureInMv

engineOnTime engineOperationStatus enginePercentageTorque engineRpm engineRunningHours

engineStartingIssueSvc engineTemperature engineTotalFuelUsed engineWorking evDte

evSportsModeStatus fastCharging frontLeftDoor frontPassengerSeatBelt frontRightDoor

fuel1 fuel2 fuel3 fuel4 fuel5 fuel fuelConsumption fuelConsumptionCounted

fuelInjectionQuantity fuelLevel fuelLevelInLitre fuelRate fuelTank fuelTankLevel

fuelType gps gsmStrength hdop hoodDoor ibutton ignition immobilizationStatus imsi

injectionQuantitySetPoint injectionTime1 injectionTime2 injectionTime

intakeAirTemperature intakeManifoldAbsolutePressure intakeMap internalStorageSize

internalStorageUsed lac lastIgnitionOnTime llsTemperature1 llsTemperature2

lockCutStatus longTimeUnlocking maxAirFlowRate maxFuelQuantity mcc milStatus mnc

motorStuck movement numberOfSatellites numDtcCodes odometer orientation parkingBrake

particleFilterPressure plugged powerCutStatus powerTakeOff prvOpenCount

prvOpenDuration ptoRpm pwmSignalOutput railPressure railPressureSetPoint

railPressureSetpoint rearCentreSeatBelt rearLeftDoor rearLeftSeatBelt rearRightDoor

rearRightSeatBelt relay retarderManual retarderState rockBreakerPedalValue

rotationCount rotationDirection rotationSpeed rssi runtimeEngineStart sdCardCid

sdCardStatus sdCardStorageSize sdCardStorageUsed seatBelt sensedBatteryVolatge

sensedBatteryVoltage serialNumber shortFuelTrim sigKeyOnIndicator simCardStatus sos

spare10 spare11 spare12 spare13 spare1 spare2 spare3 spare4 spare5 spare6 spare7

spare8 spare9 spare speed svsLampStatus t15Status t50Status tellTale0 temperature1

temperature2 temperature3 temperature4 temperature5 temperature6 temperature7

temperature8 temperature throttlePosition throttleValveActuatorPosition

timeToFullChargeMinutes timingAdvance torqueGeneratingEfi totalDistanceHighResolution

totalMileage trailer tripButton trunkDoor unauthorizedRfid updateVersion

vehicleBattery vehicleBatteryLevel vehicleVoltage washerFluidLevel

wheelbasedVehicleSpeed wifiMacAddresses wifiStrength wrongLockPassword

HEADERS

User-Authentication {{auth-token}}

PARAMS

page 1

perPage 10

Body raw (json)

json

{

"vehicleIds": ["077c6ab2-6456-4e07-abd6-1e18bbe7ba1d"],

"sensors": [

"gps",

"vehicleBatteryLevel",

"numberOfSatellites"

 ]

}

## GETGet Distance Travelled

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/distance_travelled?startTime={{startTim e}}&endTime={{endTime}}

Overview

The Vehicle Distance Travelled API allows users to retrieve the total distance travelled by a specific vehicle within a specified time range. This information can be valuable for tracking vehicle usage, analyzing efficiency, and managing maintenance schedules.

# Path Parameters

startTime (integer, required): The start timestamp of the time range in Unix epoch format.

endTime (integer, required): The end timestamp of the time range in Unix epoch format.

## Note:

1. Difference between startTime and endTime should be less than a day.

2. History data is available till last 6 months.

# Response Body

startTime (integer): The start timestamp of the requested time range.

endTime (integer): The end timestamp of the requested time range.

number (string): The unique identifier or name of the vehicle.

distance (object): An object containing the total distance travelled.

unit (string): The unit of measurement for the distance (e.g., "km" for kilometers).

value (float): The total distance travelled by the vehicle within the specified time range.

## vehicleUuid (string): The unique identifier of the vehicle.

# HEADERS

User-Authentication {{auth-token}}

PARAMS

startTime {{startTime}}

endTime {{endTime}}

# GETGet Timeline

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/timeline?startTime={{startTime}}&endTim e={{endTime}}

# Overview

The Vehicle Telematics Timeline API provides historical movement and event data for a specific vehicle within a specified time range. This documentation outlines the usage, request parameters, and response structure of the API.

## Timeline will consist of 2 main parts

1. Summary data for the provided time

2. Timeline data containing event details

## Query Parameters

startTime (required): The start time of the time range in UNIX timestamp format.

endTime (required): The end time of the time range in UNIX timestamp format.

Note:

1. Difference between startTime and endTime should be less than a day.

2. History data is available till last 6 months.

# Response Structure

The response consists of detailed information about the vehicle's movement, location, and timeline events.

startLocation : Starting location object

coordinates : lat,long coordinates of the vehicle.

address : Geo address of the vehicle at start location

endLocation : Ending coordinates of the vehicle.

coordinates : lat,long coordinates of the vehicle

address : Geo address of the vehicle at end location

motion : Details about the vehicle's motion, including distance, running time, stoppage time, offline time, and average speed.

timeline : An array of timeline events, each providing information about a specific segment of the vehicle's journey.

# Timeline Event Structure

Each timeline event includes the following details:

startLocation : Starting location object

coordinates : lat,long coordinates of the vehicle.

address : Geo address of the vehicle at start location

timestamp : Timestamp when the event started.

## endLocation : End location object

coordinates : lat,long coordinates of the vehicle.

address : Geo address of the vehicle at start location

timestamp : Timestamp when the event started.

movementStatus : Status indicating if the vehicle was moving , stopped , or offline during the event.

path : Encoded Polyline. Refer polyline below for usage and implementation

Additional details based on the movement status, such as averageSpeed and distance for moving events.

# Polyline

A polyline is a series of connected straight lines used to represent a route or path on a map. It is often encoded as a string of coordinates to reduce data size and can be decoded to display the route on mapping platforms like Google Maps.

Polyline can be drawn on google maps on both Web and mobile apps.

# Web

# 1. Set Up Google Maps JavaScript API

# 2. Decode the Polyline:

Within their JavaScript code, users can use the google.maps.geometry.encoding.decodePath()

method provided by the Google Maps JavaScript API to decode the encoded

polyline string into an array of LatLng objects representing the path.

# 3. Draw the Polyline:

Using the decoded array of LatLng objects, users can create a polyline object using

google.maps.Polyline , specifying the path, color, and other styling options. They then add this polyline to their map object using setMap() .

## App (Mobile)

1. Integrate Google Maps SDK

2. Decode the Polyline:

Within their app code, users can use the decoding functions provided by

the mapping SDK to decode the encoded polyline string into a list of

coordinates.

3. Draw the Polyline

# References

1. Polyline encode and details: Here

2. Draw polyline on map example: Here

# HEADERS

User-Authentication {{auth-token}}

PARAMS

startTime {{startTime}}

endTime {{endTime}}

Epoch time in seconds

# GETList Vehicles

https://api.a.loconav.com/integration/api/v1/vehicles?vehicleNumber={{vehicleNumber}}&page=1&perPage=10&deviceSerialNumber={{deviceSerialNumber}}&vehicleNumbers={{vehicleNumbers}}&VehicleUuids={{vehi cleUuids}}&fetchMobilizationDetails={{fetchMobilizationDetails}}

# Overview

The List Vehicles API enables users to retrieve a paginated list of vehicles along with their details like vehicle number, device details, subscription details and more.

## Request Parameters

vehicleNumber (string, optional): The vehicle number for filtering

deviceSerialNumber (string, optional): The Device serial Number (IMEI) number

page (integer): The page number for pagination. Default is 1.

perPage (integer): The number of vehicles to be included per page. Default is 10.

vehicleNumbers (string, optional):The vehicle numbers for filtering.

vehicleUuids (string, optional): The vehicleUuids for filtering.

fetchMobilizationDetails (boolean,optional): Vehicle Mobilzation Status

# Response Structure

## Each vehicle entry includes the following details:

number (string): Vehicle registration number.

deviceId (string): Unique identifier for the associated device.

displayNumber (string): Display name or identifier for the vehicle.

vehicleUuid (string): Unique identifier for the vehicle.

status (boolean): Current status of the vehicle.

current_device (object): Details about the associated device.

subscription (object): Details about the subscription, including expiration date.

vehicleType (string): Type or category of the vehicle.

createdAt (integer): Timestamp indicating when the vehicle record was created.

updatedAt (integer): Timestamp indicating when the vehicle record was last updated.

# Pagination Information

page (integer): Current page number.

perPage (integer): Number of items per page.

totalCount (integer): Total number of polygons available.

# HEADERS

User-Authentication {{auth-token}}

PARAMS

vehicleNumber {{vehicleNumber}}

fetch vehicle details by vehicle number

page 1

Page index (type: Integer) (optional, default: 1)

perPage 10

No of items per page (type: Integer) (optional, default: 10)

deviceSerialNumber {{deviceSerialNumber}}

vehicleNumbers {{vehicleNumbers}}

fetch vehicles by numbers (, seprated )

VehicleUuids {{vehicleUuids}}

fetch vehicles by Uuids (, seprated )

fetchMobilizationDetails {{fetchMobilizationDetails}}

fetch Mobilization Status

## GETGet Vehicle Score card

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/score_card?&startTime={{startTime}}&end Time={{endTime}}

# Overview

The Vehicle Score card API provides detailed insights into the behavior and performance of a vehicle within a specified time range. Fleet managers can utilize this information to assess driver efficiency, safety, and overall performance.

# Query Parameters

startTime (required): The start time of the time range in UNIX timestamp format.

endTime (required): The end time of the time range in UNIX timestamp format.

# Response Fields

runningTime : Time the vehicle spent in motion (unit: minutes).

distance : Total distance covered by the vehicle (unit: km).

stoppageTime : Time the vehicle spent in stoppage (unit: minutes).

idleDuration : Duration of engine idling (unit: minutes).

idlingEventsCount : Number of idling events.

overspeedDuration : Duration of overspeeding (unit: minutes).

overspeedEventsCount : Number of overspeed events.

suddenBrakingEventsCount : Number of sudden braking events.

suddenAccelerationEventsCount : Number of sudden acceleration events.

sharpTurnEventsCount : Number of sharp turn events.

seatBeltEventsCount : Number of seat belt events.

totalEvents : Total number of events.

overallScore : Overall driver score (unit: points, ranging from 0 to 100).

distanceMetric : Total distance covered metric (unit: km).

fuelConsumption : Fuel consumption during the specified period (unit: liters).

mileage : Vehicle mileage information (unit: km/h).

totalDuration : Total duration of the specified period (unit: minutes).

## Notes

Replace {{vehicleNumber}} , {{startTime}} , and {{endTime}} with the actual vehicle identifier and time range values, respectively.

The response provides comprehensive driving performance metrics, including running time, distance covered,stoppage time, idle duration, and various driving event counts.

The overall driving score is provided as a percentage.

This API is useful for monitoring and analyzing driver behavior and vehicle performance over a specific period.

## HEADERS

User-Authentication {{auth-token}}

PARAMS

startTime {{startTime}}

Epoch time in seconds

endTime {{endTime}}

Epoch time in seconds

## GETGet Vehicle Details

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}

## HEADERS

User-Authentication {{auth-token}}

## GETGet Live Share Link

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/live_share_link

## Overview

The Live Share Link API allows users to retrieve a shareable link for real-time tracking of a specific vehicle. This link can be shared with others to provide live updates on the vehicle's location and status.

Request Headers

User-Authentication : The authentication token for accessing the API. Replace {{auth-token}} with the actual authentication token.

### Path Parameters

vehicleId (string, required): The unique identifier of the vehicle for which the live share link is requested.

## Response Structure

shareLink (string): The generated shareable link for live tracking of the vehicle. This is a public link and can be open in any browser.

## Status Codes

200 OK : The request was successful, and the shareable link is provided.

404 Not Found : The requested vehicle was not found.

## HEADERS

User-Authentication {{auth-token}}

## Alerts

## GETGet Alerts

https://app.a.loconav.com/integration/api/v1/alerts?startTime={{startTime}}&endTime={{endTime}}&alertTyp e={{alertType}}

This endpoint sends an HTTP GET request to retrieve alerts based on the specified start time, end time, and alert type.

## Request Parameters

startTime (optional): The start time for retrieving alerts.

endTime (optional): The end time for retrieving alerts.

alertType (optional): The type of alert to be retrieved.

# Response

The response of this request is a JSON schema describing the structure of the alert data that will be returned. The JSON schema will outline the properties and their data types for the alert objects.

## Example JSON Schema:

json

{

"success": "boolean",

"data": {

"values": [

{

"id": 0,

"eventTime": 0,

"eventType": "string",

"localizeEventType": "string",

"startedTs": 0,

"startLocation": {

## HEADERS

User-Authentication {{token}}

PARAMS

startTime {{startTime}}

endTime {{endTime}}

alertType {{alertType}}

GETList Alerts

https://api.a.loconav.com/integration/api/v1/vehicles/{{vehicleId}}/alerts?startTime={{startTime}}&endTime={{endTime}}&alertType={{alertType}}

## Overview

The Get Alerts API allows users to retrieve information about alerts triggered by vehicle-related events during a specified time range.

## Request Parameters

startTime (integer, required): The timestamp indicating the start of the time range for fetching alerts.

endTime (integer, required): The timestamp indicating the end of the time range for fetching alerts.

alertType (string, optional): Filter results according to the alert type (See list below for support types)

### Note:

1. Difference between startTime and endTime should be less than a day.

2. Difference between startTime and endTime should be more than 1 min

3. startTime and endTime should not be same

4. History data is available till last 6 months.

# Response Structure

Each alert includes the following details:

id (integer): Unique identifier for the alert.

eventTime (integer): Timestamp when the event occurred.

eventType (string): Type of the alert event.

localizeEventType (string): Localized type of the alert event.

startedTs (integer): Timestamp when the alert event started.

startLocation (object): Details about the location where the alert event started.

comments (array): Additional comments related to the alert.

supportsVt (boolean): Indicates if the alert supports video tracking.

videoDetail (object): Details related to video tracking (if supported).

endedTs (integer): Timestamp when the alert event ended (if applicable).

endLocation (object): Details about the location where the alert event ended (if applicable).

value (object): Geofence information specific to the Geofence alert type. This will contain Geofence details

## Supported Alert Types

AdasCameraObstructedAlert BackCapLockAlert CrashAlert CrashDuringOverspeedAlert DeviceLowBatteryAlert DeviceMountErrorAlert DeviceOfflineAlert DeviceRemovalAlert DeviceUnpluggedAlert DisassembleAlert DistanceCoveredAlert DistanceTravelledAlert DmsCameraObstructedAlert DoorAlert DriverDistractedAlert DriverFatigueAlert DriverMobileUseAlert ElockAlert EngineCoolantTemperatureAlert EngineLoadValueAlert EngineOilTemperatureAlert EvBatteryChargingAlert EvCriticalLowBatteryAlert EvLowBatteryAlert FallAlert ForwardCollisionWarningAlert FuelLevelAlert GeofenceAlert IgnitionAlert IllegalRfidCardSwipedAlert JackKnifeAlert LaneDriftAlert LockRopeCutAlert LongTimeUnlockingAlert LowBatteryAlarmAlert LowBatteryVoltageAlert MotorStuckAlert MovementAlert OpalExoverspeedAlert OpalHarshAccelerationAlert OpalHarshBrakingAlert OpalInvalidRfidTapAlert OpalNightDrivingAlert OpalOverspeedAlert OpalSeatBeltAlert OpalSosAlert OpalTamperingAlert OverspeedAlert OverspeedWithinGeofenceAlert PossibleFuelTheftAlert PowerCutAlert PowerDisconnectedAlert PowerOffAlert PowerOnAlert RefuelingAlert RfidTapAlert RouteDeviationAlert SharpTurnAlert ShutdownAlert SosAlert SpeedLimitAlert SpeedSignViolationAlert StoppageAlert StoppageInGeofenceAlert StopSignViolationAlert SuddenAccelerationAlert SuddenBrakingAlert TailgatingAlert TemperatureSensorAlert TowAwayAlert TripDelayAlert UnwantedMovementAlert VehicleIdleAlert VehicleLowBatteryVoltageAlert WagonDetachmentAlert WrongPasswordAlert

## HEADERS

User-Authentication {{auth-token}}

PARAMS

startTime {{startTime}}

Epoch time in Seconds

endTime {{endTime}}

Epoch time in Seconds

alertType {{alertType}}

type of alert

## Polygon (Geofence)

A geofence is a virtual boundary, often a rectangular bounding box, created using mapping software with specified latitude and longitude coordinates. Integrated with fleet management and telematics, geofences trigger real-time alerts if a GPS-equipped vehicle or equipment moves beyond authorized limits, enhancing security and asset monitoring.

## Use Cases

1. Security and Alerts: Geofences can be established around construction sites where valuable equipment is stationed. If any equipment equipped with a GPS tracker is detected leaving the predefined area, immediate alerts are triggered, helping prevent theft and aiding in the recovery of the asset.

2. Delivery Route Compliance: For logistics and delivery services, geofences can be set along specified routes or delivery zones. If a delivery vehicle deviates from the planned route or enters unauthorized areas, real-time alerts ensure adherence to planned schedules and prevent potential route deviations or unauthorized stops.

## GETGet Polygon

https://api.a.loconav.com/integration/api/v1/polygons/{{polygonId}}

### Overview

The Polygon Details API allows users to retrieve information about a specific polygon defined in the system.Polygons are used for geofencing and defining specific areas of interest for tracking and monitoring purposes.

## Request Headers

User-Authentication : The authentication token for accessing the API. Replace {{auth-token}} with the actual authentication token.

# Path Parameters

polygonId (string, required): The unique identifier of the polygon for which details are requested.

# Response Body

id (integer): The unique identifier of the polygon.

name (string): The name or identifier of the polygon.

coordinates (array of strings): The center coordinates of the polygon in latitude and longitude format.

radius (integer): The radius of the polygon (if applicable).

polygonCoordinates (array of objects): The coordinates of the polygon vertices, defining its shape.

lat (string): Latitude of the vertex.

long (string): Longitude of the vertex.

# Status Codes

200 OK : The request was successful, and the polygon details are provided.

422 Unprocessable Entity : The requested polygon was not found.

# HEADERS

User-Authentication {{auth-token}}

# GETList Polygons

https://api.a.loconav.com/integration/api/v1/polygons?page=1&perPage=10&name={{name}}&active=

# Overview

The List Polygons API retrieves a paginated list of polygons based on specified query parameters. Users can filter the results by polygon name and active status.

# Request Parameters

page (integer): Page number for pagination.

perPage (integer): Number of items per page.

name (string): Filter by polygon name (optional).

active (boolean): Filter by active status (optional).

# Response Structure

Each polygon in the list includes the following details:

id (integer): Unique identifier for the polygon.

name (string): The name of the polygon.

lat (string): Latitude of the center point of the polygon.

long (string): Longitude of the center point of the polygon.

active (boolean): Indicates whether the polygon is active or not.

address (string): Address associated with the polygon.

boundingBox (array): An array of coordinates forming the bounding box of the polygon.

radius (integer): Radius of the polygon.

updatedAt (integer): Timestamp indicating when the polygon was last updated.

geofenceCategory (string): Category associated with the geofence, if available.

# Pagination Information

page (integer): Current page number.

perPage (integer): Number of items per page.

count (integer): Total number of polygons available.

## Bounding Box

The bounding box is a rectangular area defined by four coordinates. In the response, it is represented as an array of latitude and longitude pairs. The bounding box encompasses the outer edges of the circular polygon, allowing for simplified spatial queries and calculations.

# HEADERS

User-Authentication {{auth-token}}

PARAMS

page 1

page no.

perPage 10

no. of polygons on one page

name {{name}}

Name of polygon (Autocomplete)

active Status of polygon

# POSTCreate Polygon

https://api.a.loconav.com/integration/api/v1/polygons

# Overview

The Create Polygon API allows users to define and create geofence polygons with specified attributes. These polygons can be utilized for location-based services, such as monitoring and triggering events when a tracked asset enters or exits the defined area.

## Request Parameters

name (string): The name of the polygon.

lat (float): Latitude of the center point of the polygon.

long (float): Longitude of the center point of the polygon.

distanceUnit (string): Unit of measurement for the radius (e.g., "m" for meters).

radius (integer): Radius of the polygon.

active (boolean): Indicates whether the polygon is active or not.

# Response Structure

id (integer): Unique identifier for the created polygon.

name (string): The name of the polygon.

lat (string): Latitude of the center point of the polygon.

long (string): Longitude of the center point of the polygon.

active (boolean): Indicates whether the polygon is active or not.

boundingBox (array): An array of coordinates forming the bounding box of the polygon.

radius (integer): Radius of the polygon.

updatedAt (integer): Timestamp indicating when the polygon was last updated.

## Bounding Box

The bounding box is a rectangular area defined by four coordinates. In the response, it is represented as an array of latitude and longitude pairs. The bounding box encompasses the outer edges of the circular polygon, allowing for simplified spatial queries and calculations.

## HEADERS

User-Authentication {{auth-token}}

Body raw (json)


| json  |
| --- |
| {<br> "polygon":{<br> "name": "test_polygon4",<br> "lat": 10,<br> "distanceUnit": "m",<br> "radius": 100,<br> "active": true,<br> "long": 85.882186<br> }<br>} |


## PUTUpdate Polygon

https://api.a.loconav.com/integration/api/v1/polygons/671966

## Overview

The Update Polygon API allows users to modify the attributes of an existing polygon. Users can update the polygon's name, location, radius and active status.

## Request Parameters

polygonId (integer): Unique identifier for the polygon to be updated.

# Request Body

name (string): The updated name of the polygon.

lat (float): The updated latitude of the center point of the polygon.

long (float): The updated longitude of the center point of the polygon.

distanceUnit (string): The unit of measurement for the radius (e.g., "m" for meters).

radius (integer): The updated radius of the polygon.

active (boolean): The updated status indicating whether the polygon is active or not.

# Updated Polygon Structure

The updated polygon includes the following details:

id (integer): Unique identifier for the polygon.

name (string): The updated name of the polygon.

lat (string): The updated latitude of the center point of the polygon.

long (string): The updated longitude of the center point of the polygon.

active (boolean): Indicates whether the polygon is active or not.

boundingBox (array): An array of coordinates forming the bounding box of the polygon.

radius (integer): The updated radius of the polygon.

updatedAt (integer): Timestamp indicating when the polygon was last updated.

HEADERS

User-Authentication vucDSzM3NZyJx2znSmzh

Content-Type application/json

Body raw

{

"polygon":{

"name": "test_polygon5",

"lat": 90,

"distanceUnit": "m",

"radius": 100,

"active": true,

"long": 85.882186

}

}

# Trips

# GETList Trips

https://api.a.loconav.com/integration/api/v1/trips?uniqueId={{uniqueId}}&startTime={{startTime}}&endTime={{endTime}}&states={{states}}&driverId={{driverId}}&sortColumn={{sortColumn}}&sortOrder={{sortOrder}}&p age=1&perPage=10&vehicleNumber={{vehicleNumber}}

# Overview

This API allows users to retrieve a list of trips based on various filters such as unique ID, start time, end time, states,driver ID, sort column, sort order, page number, and number of trips per page.

## Query Parameters:

uniqueId (string, optional): Unique ID of the trip.

startTime (integer, optional): Start time of the trip.

endTime (integer, optional): End time of the trip.

states (string, optional): Comma-separated list of states to filter trips by. { initialized, trashed, ongoing,delayed, unsuccessful, completed }

driverId (integer, optional): ID of the driver associated with the trip.

sortColumn (string, optional): Column to sort the trips by. {shouldStartAt, createdAt}

sortOrder (string, optional): Order of sorting {asc, desc}.

page (integer, optional): Page number of the results.

perPage (integer, optional): Number of trips per page.

vehicleNumber (string, optional): Number of the vehicle associated with the trip.

# Response Structure

success (boolean): Indicates whether the request was successful.

data.values (array): Array of trip objects.

id (integer): ID of the trip.

vehicleNumber (string): Number of the vehicle associated with the trip.

vehicleId (integer): ID of the vehicle associated with the trip.

uniqueId (string): Unique ID of the trip.

shouldStartTs (integer): Start time of the trip.

createdAt (integer): Timestamp of when the trip was created.

state (string): State of the trip (e.g., "ongoing").

driver (object): Information about the driver associated with the trip.

id (integer): ID of the driver.

name (string): Name of the driver.

ownerType (string): Type of the trip owner (e.g., "Transporter").

ownerId (integer): ID of the trip owner.

ownerEmail (string): Email of the trip owner.

ownerName (string): Name of the trip owner.

creatorType (string): Type of the trip creator (e.g., "User").

creatorId (integer): ID of the trip creator.

completionPercentage (integer): Percentage of trip completion.

creatorEmail (string): Email of the trip creator.

creatorName (string): Name of the trip creator.

transporterName (string): Name of the transporter associated with the trip.

truckCurrentLocation (string): Current location of the truck associated with the trip.

customData (array): Custom data associated with the trip.

checkPoints (array): Array of checkpoint objects associated with the trip.

driverCta (object): Information about driver's call-to-action.

currentCta (object): Information about current call-to-action.

expectedDistance (integer): Expected distance of the trip.

unsuccessfulReason (string): Reason for the trip being unsuccessful.

createdVia (string): Method through which the trip was created {apis}.

routeDeviationEnabled (boolean): Indicates whether route deviation is enabled for the trip.

isSoftVehicleRoute (boolean): Indicates whether the vehicle route is soft.

## HEADERS

User-Authentication {{auth-token}}

PARAMS

uniqueId {{uniqueId}}

optional

startTime {{startTime}}

optional, Long

endTime {{endTime}}

optional, Long

states {{states}}

optional { 1 = :initialized, 2 = :trashed, 3 = :ongoing, 4 = :delayed, 5 =:unsuccessful, 6 = :completed }

driverId {{driverId}}

optional

sortColumn {{sortColumn}}

optional "should_start_at", "created_at"

sortOrder {{sortOrder}}

optional "desc", "asc"

page 1

optional

perPage 10

optional

vehicleNumber {{vehicleNumber}}

optional

## POSTCreate Trip

https://api.a.loconav.com/integration/api/v1/trips

## Overview

### Create Trip.

1. Create trip using route name: Pass route name in the create trip API.

2. Create trip using Route id: Pass route id in the create trip API.

3. Create trip using geofence: Pass geofence id in the create trip API

4. Create Trip using the address and coordinates : Pass address and coordinates in source in the create trip API

5. Create Trip where the destination is not known

6. Create Trip with multiple stops/checkpoints

### Create Trip Request

1. Removing the vehicle json object from the body of the request will create a trip request instead of trip.(Trip state will be "requested" instead of "new"). For this "trip_request" feature should be enabled for User.

### Mandatory Fields :

1. should_start_at
2. source

a. "geofence_id" or "geofence_name" or a combination of ("coordinates" and "address")

Validations:

1. etd (Estimated Time of Departure) &gt; eta (Estimated Time of Arrival)

# Cases:

1. Route[id, name], if either of id and name is present, it means we are using existing route. source, checkpoints,destination can be ignored.

2. If Route[id, name] not present, send Source and CheckPoints. Destination is optional.

a. if create_new_vehicle_route is not present, route won't be shown on UI.

b. if create_new vehicle route is present, route name is mandatory and will be shown on UI.

# Request Body

vehicle

id (integer)

number (string)

route

id (integer)

name (string)

customFields (HashMap)

uniqueId (String) will be auto generated by loconav if not given

createNewVehicleRoute (boolean)

newVehicleRouteName (string)

shouldStartAt (integer, epoch timestamp) Time by which trip should be started

expectedDistance (integer)

tripDelayAlertsEnabled (boolean)

sourceName (string)

destinationName (string)

shouldExpireOldTrips (boolean) Mark True if you want to expire all active trips on the vehicle.

# checkPoints

geofenceId (integer)

geofenceName (string)

eta (integer, epoch timestamp in seconds)

etd (integer, epoch timestamp in seconds)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

tasks: (object) explained below

source

geofenceId (integer)

geofenceName (string)

eta (integer)

etd (integer)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

tasks: (object) explained below

checkPointTargetOption

activity (integer) # unloading: 0, loading: 1, maintenance: 2, fuel: 3, partialLoading: 4,

partialUnloading: 5, parking

odometerIn (integer)

odometerOut (integer)

fuelIn (integer)

fuelOut (integer)

destination

geofenceId (integer)

geofenceName (string)

eta (integer)

etd (integer)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

tasks: (object) explained below

cosigner

id (integer) # Company Id

name (string)

expectedPolylineIds (list) # List of google polyline data.

tasks:

taskTemplateId (Integer)

fields:

fieldId: (integer)

value: (string)

fieldGroups

fieldGroupId: (integer)

fields:

fieldId: (integer)

value: (string)

# Response Structure

success (boolean)

data

id (integer): Trip Id generated by loconav

uniqueId (string)

## HEADERS

User-Authentication {{auth-token}}

Body raw (json)

json

{

"trip": {

"vehicle": {

"number": "VT_MOCKER2"

},

"customFields": {},

"createNewVehicleRoute": true,

"newVehicleRouteName": "test_test_route_12",

"shouldStartAt": 1706264834,

"uniqueId": "test_01",

"expectedDistance": 30,

"tripDelayAlertsEnabled": true,

"sourceName": "Gurugram",

"shouldExpireOldTrips": false,

"source": {

"address": "test_address",

"coordinates": "10.01,10.01",

"radius": 10,

"eta": 1706285834,

"etd": 1706287834

}

 }

}

## PUTUpdate Trip

https://api.a.loconav.com/integration/api/v1/trips/{{tripId}}

## Overview

This API endpoint allows users to update trip details such as the source location and actions.

### Action can have these 4 values

1. UPDATE_TRIP - Can update any variables

a. Mandatory Fields : action, source

2. END_TRIP - To end the trip: Only need "id" for this.

a. Mandatory Fields : action, source

3. PARTIAL_UPDATE_TRIP - Can be used to update "custom_fields" only.

a. Mandatory Fields : action, custom_fields

4. REJECT_TRIP - To reject a trip which is in requested state.

a. Mandatory Fields: action

5. START_TRIP - To start the trip: Only need "id" for this.

a. Mandatory Fields : action

# Path Variables

tripId (integer): Unique identifier for the trip to be deleted.

# Request Body

action (string, required)

newVehicleRouteName (string)

shouldStartAt (integer, epoch timestamp) Time by which trip should be started

expectedDistance (integer)

tripDelayAlertsEnabled (boolean)

sourceName (string)

destinationName (string)

shouldExpireOldTrips (boolean) Mark True if you want to expire all active trips on the vehicle.

checkPoints

geofenceId (integer)

geofenceName (string)

eta (integer, epoch timestamp in seconds)

etd (integer, epoch timestamp in seconds)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

source

geofenceId (integer)

geofenceName (string)

eta (integer)

etd (integer)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

checkPointTargetOption

activity (integer) # unloading: 0, loading: 1, maintenance: 2, fuel: 3, partialLoading: 4,

partialUnloading: 5, parking

odometerIn (integer)

odometerOut (integer)

fuelIn (integer)

fuelOut (integer)

destination

geofenceId (integer)

geofenceName (string)

eta (integer)

etd (integer)

coordinates (string, lat,long)

address (string)

createGatepass (boolean)

cosigner

id (integer) # Company Id

name (string)

expectedPolylineIds (list) # List of google polyline data.

# Response Structure

success (boolean)

data

id (integer): Trip Id generated by loconav

uniqueId (string)

# Notes

Replace {trip_id} in the URL with the actual ID of the trip to be updated.

HEADERS

User-Authentication {{auth-token}}

Content-Type application/json

<!-- Body raw -->

{

"trip": {

"action": "START_TRIP",

"source": {

"address": "test_address",

"coordinates": "10.01,10.01",

"radius": 10,

"eta": 1706285834,

"etd": 1706287834

}

 }

}

# DELETEDelete Trip

https://api.a.loconav.com/integration/api/v1/trips/{{tripId}}

# Overview

This API endpoint allows administrators to delete a trip based on its ID.

# Request Parameters

tripId (integer): Unique identifier for the trip to be deleted.

# Response Structure

success (boolean): Indicates whether the request was successful.

message (string): A message confirming the success of the deletion operation.

## Notes

Replace {trip_id} in the URL with the actual ID of the trip to be deleted.

## HEADERS

User-Authentication {{auth-token}}

## GETGet Trip Track Url

https://api.a.loconav.com/integration/api/v1/trips/{{tripId}}/track_url?allCheckPoints={{boolean}}&checkPoint Ids={{array}}

# Overview

This API endpoint retrieves a public tracking URL for a specific trip, including given checkpoints, allowing users to monitor the trip's progress in real-time.

Clients can send this URL directly to end customers for real time public tracking of the vehicle.

## Path Parameters

{trip_id} (integer): ID of the trip for which the tracking URL is requested.

### Query Parameters

allCheckPoints (boolean): Indicates whether to include all checkpoints in the tracking URL. Set to true to include all checkpoints.

checkPointIds (array of integer): If allCheckPoints param is false then user need to pass geofence ids that were passed in Create Trip API. (Eg: [23,45]). The map will only shows the mentioned check points.

# Response Structure

success (boolean): Indicates whether the request was successful.

data

tripTrackToken (string): Token used to track the trip.

url (string): Tracking URL for the trip.

HEADERS

User-Authentication {{user_auth}}

Content-Type application/json

PARAMS

allCheckPoints {{boolean}}

checkPointIds {{array}}

Users

## GETGet User Details

https://api.a.loconav.com/integration/api/v1/user

## Overview

The User Details API allows users to retrieve detailed information about the currently authenticated user in the LocoNav system. This information includes the user's name, email, phone numbers, role, and account details.

## Request Headers

User-Authentication : The authentication token for accessing the API. Replace {{auth-token}} with the actual authentication token.

# Response Fields

id (integer): The unique identifier of the user.

name (string): The name of the user.

email (string): The email address of the user.

createdAt (string): The timestamp of when the user account was created.

updatedAt (string): The timestamp of when the user account was last updated.

phoneNumbers (string): The phone numbers associated with the user.

role (string): The role of the user in the system.

## account (object): An object containing details about the user's account.

id (integer): The unique identifier of the user's account.

name (string): The name of the user's account.

email (string): The email address of the user's account.

createdAt (string): The timestamp of when the user's account was created.

updatedAt (string): The timestamp of when the user's account was last updated.

active (boolean): Indicates if the user's account is active.

alertsPusher (boolean): Indicates if the user has alerts pusher enabled.

## HEADERS

User-Authentication {{auth-token}}

## FAQs

## Q: How do I authenticate my requests to the APIs?

A: You can authenticate your requests by including an User auth token in the request headers.Refer to the Authentication mechanism in API documentation for specific authentication methods and requirements.

## Q: What data formats are supported for request and response payloads?

A: The APIs support JSON format for request and response payloads. Refer to the API documentation for details on supported data formats.

Q: Is there any limit on the number of requests I can make to the APIs?

A: Yes, there are rate limits enforced on API usage to prevent abuse and maintain system performance. If you exceed the rate limits, you may receive a 429 Too Many Requests error. Refer to the API documentation for information on rate limits and how to handle them.

## Q: How can I handle pagination for listing APIs?

A: Listing APIs are paginated to manage large datasets efficiently. You can specify query parameters such as page number and items per page to navigate through paginated results. Refer to the API documentation for pagination parameters and usage instructions.

## Q: What should I do if I encounter errors while using the APIs?

A: If you encounter errors, first ensure that your request parameters and authentication credentials are correct. Check the API documentation for information on error codes and descriptions to troubleshoot the issue. If you're unable to resolve the issue, contact support for assistance.

## Q: Can I receive real-time notifications for specific events using webhooks?

A: Yes, you can subscribe to webhooks to receive real-time notifications for events such as alerts (e.g., speeding, geofence entry/exit) and live location updates. Refer to the API documentation for webhook endpoints for alerts and live location.

## Q: How can I ensure data security and privacy when using the APIs?

A: APIs are accessed over HTTPS, ensuring that all data transmitted between your application and our servers is encrypted. To maintain system stability and prevent abuse, we implement rate limiting on our APIs. We use auth tokens to authenticate requests from clients. This ensures that only authorized users or applications can access our API endpoints

## Alerts Subscriptions

## GETGet Alert Subscriptions

https://app.a.loconav.com/integration/api/v1/vehicles/{{vehicle_uuid}}/alerts/subscriptions?type={{type}}

## HEADERS

User-Authentication {{token}}

PARAMS

type {{type}}








