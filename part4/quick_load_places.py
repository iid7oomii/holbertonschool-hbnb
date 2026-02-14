"""
Simple script to add places directly through API
"""
import requests
import json

API_URL = 'http://127.0.0.1:8000/api/v1'

# First, login to get admin token
login_data = {
    'email': 'admin@hbnb.com',
    'password': 'admin123'
}

print("Logging in as admin...")
response = requests.post(f'{API_URL}/users/login', json=login_data)

if response.status_code != 200:
    print("✗ Login failed. Admin user might not exist.")
    exit(1)

token = response.json()['access_token']
print("✓ Login successful")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Get admin user ID
response = requests.get(f'{API_URL}/users/', headers=headers)
users = response.json()
admin = next((u for u in users if u['email'] == 'admin@hbnb.com'), None)

if not admin:
    print("✗ Admin user not found")
    exit(1)

admin_id = admin['id']
print(f"✓ Admin ID: {admin_id}")

# Create places without amenities for simplicity
print("\nCreating places...")
places_data = [
    {
        'title': 'Luxury Beach Villa',
        'description': 'Beautiful beachfront property with stunning ocean views',
        'price': 250.00,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': admin_id,
        'amenities': []
    },
    {
        'title': 'Cozy Mountain Cabin',
        'description': 'Perfect retreat in the mountains with hiking trails nearby',
        'price': 120.00,
        'latitude': 39.7392,
        'longitude': -104.9903,
        'owner_id': admin_id,
        'amenities': []
    },
    {
        'title': 'Modern City Apartment',
        'description': 'Stylish apartment in the heart of downtown',
        'price': 180.00,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'owner_id': admin_id,
        'amenities': []
    },
    {
        'title': 'Rustic Country House',
        'description': 'Peaceful countryside home perfect for family getaways',
        'price': 95.00,
        'latitude': 42.3601,
        'longitude': -71.0589,
        'owner_id': admin_id,
        'amenities': []
    },
    {
        'title': 'Downtown Loft',
        'description': 'Modern loft in the city center with great nightlife',
        'price': 150.00,
        'latitude': 41.8781,
        'longitude': -87.6298,
        'owner_id': admin_id,
        'amenities': []
    }
]

place_ids = []
for place_data in places_data:
    response = requests.post(f'{API_URL}/places/', json=place_data, headers=headers)
    if response.status_code == 201:
        place_id = response.json()['id']
        place_ids.append(place_id)
        print(f"✓ Place created: {place_data['title']} (${place_data['price']}/night)")
    else:
        print(f"✗ Failed to create: {place_data['title']}")
        print(f"  Error: {response.status_code} - {response.text[:200]}")

print("\n" + "="*60)
print(f"✓ Successfully created {len(place_ids)} places!")
print("="*60)
print("\nNow you can:")
print("  1. Refresh the web page: part4/web_client/index.html")
print("  2. You should see the places list")
print("  3. Try the price filter")
print("  4. Click 'View Details' on any place")
print("\nLogin credentials:")
print("  Email: admin@hbnb.com")
print("  Password: admin123")
