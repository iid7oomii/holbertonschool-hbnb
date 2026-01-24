from __future__ import annotations

import re
from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import bcrypt

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    User entity:
    - first_name (required, max 50)
    - last_name  (required, max 50)
    - email      (required, valid format)
    - password   (required, hashed)
    - is_admin   (bool, default False)
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_admin: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._password = None
        if password:
            self.hash_password(password)
        self.validate()

    def hash_password(self, password: str) -> None:
        """Hash the password using bcrypt"""
        if not password:
            raise ValueError("password is required")
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hashed password"""
        if not self._password:
            return False
        return bcrypt.check_password_hash(self._password, password)

    @property
    def password(self) -> str:
        """Getter for password - returns the hashed password"""
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Setter for password - hashes the password"""
        self.hash_password(value)

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