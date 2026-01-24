"""
Flask extensions initialization module.
Extensions are created here without binding to app,
then initialized in the application factory.
"""
from flask_bcrypt import Bcrypt

# Create extension instance without binding to app
bcrypt = Bcrypt()
