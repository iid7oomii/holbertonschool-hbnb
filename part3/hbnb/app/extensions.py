"""
Flask extensions initialization module.
Extensions are created here without binding to app,
then initialized in the application factory.
"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create extension instances without binding to app
bcrypt = Bcrypt()
jwt = JWTManager()
