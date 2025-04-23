import requests
import json

# Base URL
base_url = "http://localhost:8000/api"

# Your authentication token - replace with your actual token
auth_token = "f806b008d1f44e825b904af1642d44e48c13799d"

# Headers for authentication
headers = {
    "Authorization": f"Token {auth_token}",
    "Content-Type": "application/json"
}

# 1. Create a delivery person
def create_delivery_person():
    # Update this path based on how you configured your URLs
    endpoint = f"{base_url}/shipments/delivery-persons/"  # This should match your URL structure
    data = {
        "user_id": 1,  # Replace with an actual user ID
        "phone_number": "555-123-4567",
        "vehicle_info": "Toyota Prius (2020)"
    }
    
    response = requests.post(endpoint, headers=headers, json=data)
    print(f"Create delivery person status code: {response.status_code}")
    print(f"Response: {response.json() if response.status_code < 400 else response.text}")
    return response.json() if response.status_code < 400 else None

# 2. Assign a delivery person to a shipment
def assign_delivery_person(shipment_id, delivery_person_id):
    endpoint = f"{base_url}/shipments/{shipment_id}/assign_delivery/"
    data = {
        "delivery_person_id": delivery_person_id
    }
    
    response = requests.post(endpoint, headers=headers, json=data)
    print(f"Assign delivery status code: {response.status_code}")
    print(f"Response: {response.json() if response.status_code < 400 else response.text}")

if __name__ == "__main__":
    # First create a delivery person
    delivery_person = create_delivery_person()
    
    if delivery_person:
        # Then assign them to shipment 28
        assign_delivery_person(28, delivery_person["id"])
    else:
        print("Failed to create delivery person")