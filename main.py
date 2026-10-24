from job import Job
from housing import Housing
import calculations as calc
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

dream_job = Job("Genius Inc.", "Scientist", "Sunnyvale", 200000, ['Monday', 'Tuesday', 'Thursday'], "Accepted" )
awful_job = Job("Evil Corp.", "Villain", "Nightmare Town", 0, ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], "Denied" )
specific_address_job = Job("Google", "Tech", 
                           "Google Building MP3, 1170 Bordeaux Dr Building 3, Sunnyvale, CA 94089",
                           300000, ['Monday', 'Tuesday', 'Thursday'], "Pending")

dream_house = Housing("Happy Home", "Sunnyvale", 1500, 10, "Accepted")
awful_house = Housing("Bad Place", "Fresno", 5000, 1, "Denied")
specific_address_house =  Housing("Winchester Mystery House", 
                                  "525 S Winchester Blvd, San Jose, CA 95128",
                                  15000, 9, "Pending")
MORNING_ARIVAL_TIME = '09:00'
EVENING_DEPARTURE_TIME = "2026-10-26T17:00:00-07:00"

def estimate_departure_formatted(time_estimate, arrival_time = MORNING_ARIVAL_TIME):
    arrival = datetime.strptime(arrival_time, "%H:%M")
    duration = timedelta(seconds=time_estimate)
    departure = arrival - duration
    return f"2026-10-26T{departure.strftime("%H:%M:%S")}-07:00"

def estimate_departure(time_estimate, arrival_time = MORNING_ARIVAL_TIME):
    arrival = datetime.strptime(arrival_time, "%H:%M")
    duration = timedelta(seconds=time_estimate)
    departure = arrival - duration
    return departure.strftime("%H:%M")

def build_request_body_morning(job,housing,duration):
    morning_departure_time = calc.estimate_departure(duration)
    request_body_morning = {
    "origin": {
        "address": housing.location
    },
    "destination": {
        "address": job.location
    },
    "travelMode": "DRIVE",
    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
    "departureTime": morning_departure_time
    }
    return request_body_morning

def build_request_body_evening(job,housing,departure_time = EVENING_DEPARTURE_TIME):
    request_body_evening = {
    "origin": {
        "address": job.location
    },
    "destination": {
        "address": housing.location
    },
    "travelMode": "DRIVE",
    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
    "departureTime": departure_time
    }
    return request_body_evening    

def response_distance_duration(request_body):
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"   
    
    response = requests.post(
    url,
    headers=headers,
    json=request_body,
    timeout=20
    )
    return response


def generate_report(job,housing):
    request_body = build_request_body_evening(job,housing)

    response = response_distance_duration(request_body)

    response.raise_for_status()
    data = response.json()

    if not data.get("routes",[]):
        print("no routes found")
        return

    route = data["routes"][0]
    distance_miles = calc.meters_to_miles(route["distanceMeters"])
    time = calc.duration_to_seconds(route["duration"])
    time_formatted = calc.seconds_to_display(time*2)
    days_per_week = len(job.onsite_days)
    cost_per_trip = calc.calculate_gas_cost(distance_miles,40,5.79)
    cost_per_week = days_per_week * 2 * cost_per_trip
    morning_departure_time = calc.estimate_departure(time,  MORNING_ARIVAL_TIME)
    departure = datetime.fromisoformat(morning_departure_time)
    print(f"Generating Report for Job: {job.name} and Housing: {housing.name}")
    print(f"Estimated round trip travel time: {time_formatted}, {days_per_week} days per week")
    print(f"Expect to leave around {departure.strftime('%H:%M')}am")
    print(f"Approximate weekly gas cost: ${cost_per_week:.2f}")


    return

generate_report(specific_address_job, specific_address_house)