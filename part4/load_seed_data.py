"""
Data loader to seed the application with initial data from JSON file
This runs automatically when the Flask app starts
"""
import json
import os
from hbnb.app.services.facade import HBnBFacade
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review


def load_seed_data():
    """Load seed data from JSON file into the repositories"""
    
    # Get the path to seed_data.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    seed_file = os.path.join(current_dir, 'seed_data.json')
    
    # Check if seed file exists
    if not os.path.exists(seed_file):
        print("  Seed data file not found. Skipping data loading.")
        return
    
    # Load JSON data
    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f" Error loading seed data: {e}")
        return
    
    facade = HBnBFacade()
    
    # Track created objects
    users_map = {}
    amenities_map = {}
    places_map = {}
    
    print("\n" + "="*60)
    print(" Loading seed data...")
    print("="*60)
    
    # 1. Create Users
    print("\n Creating users...")
    for user_data in data.get('users', []):
        try:
            # Check if user already exists
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                users_map[user_data['email']] = existing_user
                print(f"  ✓ User exists: {user_data['email']}")
                continue
            
            # Create new user
            new_user = facade.create_user(user_data)
            users_map[user_data['email']] = new_user
            print(f"  ✓ Created user: {user_data['email']}")
        except Exception as e:
            print(f"  ✗ Error creating user {user_data['email']}: {e}")
    
    # 2. Create Amenities
    print("\n Creating amenities...")
    for amenity_data in data.get('amenities', []):
        try:
            # Check if amenity exists
            existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
            if existing_amenity:
                amenities_map[amenity_data['name']] = existing_amenity
                print(f"  ✓ Amenity exists: {amenity_data['name']}")
                continue
            
            # Create new amenity
            new_amenity = facade.create_amenity(amenity_data)
            amenities_map[amenity_data['name']] = new_amenity
            print(f"  ✓ Created amenity: {amenity_data['name']}")
        except Exception as e:
            print(f"  ✗ Error creating amenity {amenity_data['name']}: {e}")
    
    # 3. Create Places
    print("\n Creating places...")
    for place_data in data.get('places', []):
        try:
            # Get owner email and find user
            owner_email = place_data.pop('owner_email')
            owner = users_map.get(owner_email)
            
            if not owner:
                print(f"  ✗ Owner not found: {owner_email}")
                continue
            
            # Get amenity names
            amenity_names = place_data.pop('amenities', [])
            
            # Create Place object directly
            new_place = Place(
                title=place_data['title'],
                description=place_data['description'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
            )
            
            # Add amenities to place
            for amenity_name in amenity_names:
                amenity = amenities_map.get(amenity_name)
                if amenity:
                    new_place.add_amenity(amenity)
            
            # Add to repository
            facade.place_repo.add(new_place)
            
            places_map[new_place.title] = new_place
            print(f"  ✓ Created place: {new_place.title} (${new_place.price}/night)")
        except Exception as e:
            print(f"  ✗ Error creating place {place_data.get('title', '?')}: {e}")
    
    # 4. Create Reviews
    print("\n Creating reviews...")
    for review_data in data.get('reviews', []):
        try:
            # Get place and user
            place_title = review_data.pop('place_title')
            user_email = review_data.pop('user_email')
            
            place = places_map.get(place_title)
            user = users_map.get(user_email)
            
            if not place:
                print(f"  ✗ Place not found: {place_title}")
                continue
            
            if not user:
                print(f"  ✗ User not found: {user_email}")
                continue
                
            # Create Review object directly
            new_review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                place=place,
                user=user
            )
            
            # Add to repository
            facade.review_repo.add(new_review)
            
            # Add review to place
            place.add_review(new_review)
            
            print(f"  ✓ Created review for: {place_title}")
        except Exception as e:
            print(f"  ✗ Error creating review: {e}")
    
    print("\n" + "="*60)
    print(" Seed data loaded successfully!")
    print("="*60)
    print(f"   Users: {len(users_map)}")
    print(f"   Amenities: {len(amenities_map)}")
    print(f"   Places: {len(places_map)}")
    print(f"   Reviews: {len(data.get('reviews', []))}")
    print("="*60 + "\n")


if __name__ == '__main__':
    # For testing - create app context and load data
    from run import app
    with app.app_context():
        load_seed_data()
