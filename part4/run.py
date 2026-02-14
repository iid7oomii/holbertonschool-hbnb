#!/usr/bin/env python3
"""
Run script for the HBnB application.
"""
import os
from hbnb.app import create_app

# Get configuration from environment variable or use default
config_name = os.getenv('FLASK_ENV', 'development')
config_class = f'config.{config_name.capitalize()}Config' if config_name != 'development' else 'config.DevelopmentConfig'

app = create_app(config_class)

# Load seed data on first run
with app.app_context():
    try:
        from load_seed_data import load_seed_data
        load_seed_data()
    except Exception as e:
        print(f"⚠️  Could not load seed data: {e}")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=app.config.get('DEBUG', False)
    )
