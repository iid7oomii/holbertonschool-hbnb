"""
Script to initialize the database and create all tables.
Run this once before starting the application.
"""
import sys
import os

# Add the part3 directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from hbnb.app import db

# Import models to register them with SQLAlchemy
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully!")
        print(f"✓ Database file: {os.path.join(os.getcwd(), 'development.db')}")
        
        # List all tables created
        print("\nTables created:")
        print("  - users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)")
