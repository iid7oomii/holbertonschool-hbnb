"""
Add sample data to the database for testing the web client
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from hbnb.app import db
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review

def add_sample_data():
    with app.app_context():
        # Check if data already exists
        existing_places = Place.query.all()
        if len(existing_places) > 0:
            print(f"✓ Database already has {len(existing_places)} places")
            return
        
        # Get or create admin user
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if not admin:
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@hbnb.com',
                is_admin=True
            )
            admin.hash_password('admin123')
            db.session.add(admin)
        
        # Create sample user
        user1 = User(
            first_name='Saleh',
            last_name='Alshaikh',
            email='Saleh@hero.com'
        )
        user1.hash_password('hero123')
        db.session.add(user1)
        
        # Create amenities
        wifi = Amenity(name='WiFi')
        pool = Amenity(name='Swimming Pool')
        parking = Amenity(name='Free Parking')
        gym = Amenity(name='Gym')
        
        db.session.add_all([wifi, pool, parking, gym])
        db.session.commit()
        
        # Create sample places
        place1 = Place(
            title='Luxury Beach Villa',
            description='Beautiful beachfront property with stunning ocean views',
            price=250.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner=admin
        )
        place1.amenities = [wifi, pool, parking]
        db.session.add(place1)
        
        place2 = Place(
            title='Cozy Mountain Cabin',
            description='Perfect retreat in the mountains with hiking trails nearby',
            price=120.00,
            latitude=39.7392,
            longitude=-104.9903,
            owner=user1
        )
        place2.amenities = [wifi, parking]
        db.session.add(place2)
        
        place3 = Place(
            title='Modern City Apartment',
            description='Stylish apartment in the heart of downtown',
            price=180.00,
            latitude=40.7128,
            longitude=-74.0060,
            owner=admin
        )
        place3.amenities = [wifi, gym, parking]
        db.session.add(place3)
        
        db.session.commit()
        
        # Add sample reviews
        review1 = Review(
            text='Amazing place! Highly recommended.',
            rating=5,
            place=place1,
            user=user1
        )
        db.session.add(review1)
        
        review2 = Review(
            text='Great location and very clean.',
            rating=4,
            place=place2,
            user=admin
        )
        db.session.add(review2)
        
        review3 = Review(
            text='Perfect for a city getaway!',
            rating=5,
            place=place3,
            user=user1
        )
        db.session.add(review3)
        
        db.session.commit()
        
        print("✓ Sample data added successfully!")
        print(f"  - 2 users created (admin@hbnb.com, Saleh@hero.com)")
        print(f"  - 4 amenities created")
        print(f"  - 3 places created")
        print(f"  - 3 reviews created")
        print("\nYou can now test the web client!")
        print("Login credentials:")
        print("  Email: admin@hbnb.com")
        print("  Password: admin123")

if __name__ == '__main__':
    add_sample_data()
