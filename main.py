from job import Job
from housing import Housing
import calculations as calc
import os
from dotenv import load_dotenv
import requests

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

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")


def generate_report(job,housing):

    request_body = {
    "origin": {
        "address": job.location
    },
    "destination": {
        "address": housing.location
    },
    "travelMode": "DRIVE"
    }
    
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
    response.raise_for_status()
    data = response.json()
    route = data["routes"][0]
    distance_miles = calc.meters_to_miles(route["distanceMeters"])
    time = calc.duration_to_seconds(route["duration"])
    time_formatted = calc.seconds_to_display(time)
    days_per_week = len(job.onsite_days)
    cost_per_trip = calc.calculate_gas_cost(distance_miles,40,5.79)
    cost_per_week = days_per_week * 2 * cost_per_trip
    print(f"Generating Report for {job.name} and {housing.name}")
    print(f"Estimated travel time: {time_formatted}, {days_per_week} days per week")
    print(f"Approximate weekly gas cost: ${cost_per_week:.2f}")

    return

generate_report(specific_address_job, specific_address_house)