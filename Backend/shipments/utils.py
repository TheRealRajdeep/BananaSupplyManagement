import requests
from django.conf import settings

def get_optimized_route(origin: str, destination: str) -> dict:
    """
    Calls Google Directions API to compute optimized driving route.
    Returns distance, duration, and step-by-step instructions.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "optimizeWaypoints": "true",
        "key": settings.GOOGLE_MAPS_API_KEY,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if data.get("status") != "OK" or not data.get("routes"):
        return {}
    leg = data["routes"][0]["legs"][0]
    return {
        "distance": leg["distance"],
        "duration": leg["duration"],
        "steps": [step["html_instructions"] for step in leg["steps"]],
    }

def get_map_url(lat: float, lon: float, destination: str) -> str:
    """
    Generate a Google Maps directions URL from lat/lon to destination.
    """
    origin_str = f"{lat},{lon}"
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_str}&destination={destination}"
        f"&key={settings.GOOGLE_MAPS_API_KEY}"
    )
