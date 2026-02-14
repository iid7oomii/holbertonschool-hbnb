"""
Add sample data through the API to populate InMemoryRepository
This ensures data is available for the web client
"""
import requests
import json

API_URL = 'http://127.0.0.1:8000/api/v1'

# First, login to get token
login_data = {
    'email': 'admin@hbnb.com',
    'password': 'admin123'
}

print("Logging in...")
response = requests.post(f'{API_URL}/users/login', json=login_data)
if response.status_code == 200:
    token = response.json()['access_token']
    print(f"✓ Login successful, token obtained")
else:
    print("✗ Login failed. Make sure admin user exists.")
    print("Creating admin user first...")
    
    # Create admin user
    admin_data = {
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@hbnb.com',
        'password': 'admin123'
    }
    
    response = requests.post(f'{API_URL}/users/', json=admin_data)
    if response.status_code == 201:
        print("✓ Admin user created")
        # Login again
        response = requests.post(f'{API_URL}/users/login', json=login_data)
        token = response.json()['access_token']
    else:
        print(f"✗ Failed to create admin: {response.text}")
        exit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Create regular user
print("\nCreating additional user...")
user_data = {
    'first_name': 'Ahmed',
    'last_name': 'alghamdi',
    'email': '	Ahmed@Alghamdi.com',
    'password': 'ahmed123'
}

response = requests.post(f'{API_URL}/users/', json=user_data)
if response.status_code == 201:
    user_id = response.json()['id']
    print(f"✓ User created: {user_id}")
else:
    # User might already exist, get all users to find ID
    response = requests.get(f'{API_URL}/users/', headers=headers)
    users = response.json()
    ahmed = next((u for u in users if u['email'] == 'Ahmed@Alghamdi.com'), None)
    if ahmed:
        user_id = ahmed['id']
        print(f"✓ User already exists: {user_id}")
    else:
        print("✗ Failed to create or find user")
        user_id = None

# Get admin ID
response = requests.get(f'{API_URL}/users/', headers=headers)
users = response.json()
admin = next(u for u in users if u['email'] == 'admin@hbnb.com')
admin_id = admin['id']

# Create amenities
print("\nCreating amenities...")
amenities = ['WiFi', 'Swimming Pool', 'Free Parking', 'Gym']
amenity_ids = []

for amenity_name in amenities:
    amenity_data = {'name': amenity_name}
    response = requests.post(f'{API_URL}/amenities/', json=amenity_data, headers=headers)
    if response.status_code == 201:
        amenity_id = response.json()['id']
        amenity_ids.append(amenity_id)
        print(f"✓ Amenity created: {amenity_name}")
    else:
        # Amenity might exist, get all
        response = requests.get(f'{API_URL}/amenities/')
        all_amenities = response.json()
        existing = next((a for a in all_amenities if a['name'] == amenity_name), None)
        if existing:
            amenity_ids.append(existing['id'])
            print(f"✓ Amenity exists: {amenity_name}")

# Create places
print("\nCreating places...")
places_data = [
    {
        'title': 'Luxury Beach Villa',
        'description': 'Beautiful beachfront property with stunning ocean views',
        'price': 250.00,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': admin_id,
        'amenities': amenity_ids[:3] if len(amenity_ids) >= 3 else amenity_ids
    },
    {
        'title': 'Cozy Mountain Cabin',
        'description': 'Perfect retreat in the mountains with hiking trails nearby',
        'price': 120.00,
        'latitude': 39.7392,
        'longitude': -104.9903,
        'owner_id': user_id if user_id else admin_id,
        'amenities': amenity_ids[:2] if len(amenity_ids) >= 2 else amenity_ids
    },
    {
        'title': 'Modern City Apartment',
        'description': 'Stylish apartment in the heart of downtown',
        'price': 180.00,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'owner_id': admin_id,
        'amenities': amenity_ids if amenity_ids else []
    }
]

place_ids = []
for place_data in places_data:
    response = requests.post(f'{API_URL}/places/', json=place_data, headers=headers)
    if response.status_code == 201:
        place_id = response.json()['id']
        place_ids.append(place_id)
        print(f"✓ Place created: {place_data['title']}")
    else:
        print(f"✗ Failed to create place: {place_data['title']}")
        print(f"  Error: {response.text}")

# Add reviews
if place_ids and user_id:
    print("\nAdding reviews...")
    reviews_data = [
        {
            'text': 'Amazing place! Highly recommended.',
            'rating': 5,
            'place_id': place_ids[0]
        },
        {
            'text': 'Great location and very clean.',
            'rating': 4,
            'place_id': place_ids[1] if len(place_ids) > 1 else place_ids[0]
        }
    ]
    
    for review_data in reviews_data:
        response = requests.post(f'{API_URL}/reviews/', json=review_data, headers=headers)
        if response.status_code == 201:
            print(f"✓ Review added")
        else:
            print(f"✗ Failed to add review: {response.text}")

print("\n" + "="*50)
print("✓ Sample data loaded successfully!")
print("="*50)
print("\nYou can now use the web client:")
print("  - Open: part4/web_client/index.html")
print("\nLogin credentials:")
print("  Email: admin@hbnb.com")
print("  Password: admin123")
print("\n  Email: Ahmed@Alghamdi.com")
print("  Password: ahmed123")
