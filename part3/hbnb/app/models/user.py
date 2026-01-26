from __future__ import annotations

import re
from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import bcrypt
from hbnb.app import db

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    SQLAlchemy User Model:
    - first_name (required, max 50)
    - last_name  (required, max 50)
    - email      (required, valid format, unique)
    - password   (required, hashed)
    - is_admin   (bool, default False)
    """
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        is_admin: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        # Password should be set using hash_password() method after initialization
        self.password = None
        self.validate()

    def hash_password(self, password: str) -> None:
        """Hash the password using bcrypt"""
        if not password:
            raise ValueError("password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hashed password"""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def validate(self) -> None:
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name is required")
        if len(self.first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")

        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name is required")
        if len(self.last_name) > 50:
            raise ValueError("last_name must be at most 50 characters")

        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email is required")
        if not _EMAIL_RE.match(self.email.strip()):
            raise ValueError("email must be a valid email address")

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")

    def to_dict(self):
        """Return a dictionary representation without password"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at),
            'updated_at': self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else str(self.updated_at)
        }