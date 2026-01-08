# HBnB Project

## Project Overview
This project is a Flask-based API for the HBnB application. The project follows a **modular architecture** with clear separation of concerns:

- **app/**: Main application package
  - **api/v1/**: API endpoints organized by resource (users, places, reviews, amenities)
  - **models/**: Data models for users, places, reviews, amenities
  - **services/**: Business logic layer, including the HBnBFacade for centralized access
  - **persistence/**: Data storage layer (In-Memory Repository)
- **run.py**: Entry point to run the Flask application
- **config.py**: Application configuration settings
- **requirements.txt**: List of required Python packages
- **README.md**: Project documentation

## Installation
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
