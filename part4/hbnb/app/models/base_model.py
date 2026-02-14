


from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any
from hbnb.app import db


class BaseModel(db.Model):
    """
    SQLAlchemy Base Model providing:
    - id (UUID string, primary key)
    - created_at (UTC datetime)
    - updated_at (UTC datetime)
    - save(): updates updated_at
    - update(data): set attributes then validate
    """
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize with fallback for non-SQLAlchemy usage"""
        super().__init__(**kwargs)
        # Ensure dates are set even when not using SQLAlchemy session
        if not hasattr(self, 'id') or self.id is None:
            self.id = str(uuid.uuid4())
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'updated_at') or self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def save(self) -> None:
        """Update the updated_at timestamp and commit to database"""
        self.updated_at = datetime.utcnow()
        try:
            db.session.commit()
        except:
            # If not in a session context, just update the timestamp
            pass

    def validate(self) -> None:
        """Override in subclasses."""
        return

    def update(self, data: dict[str, Any]) -> None:
        """
        Update allowed attributes (ignore id/created_at), then validate and save.
        """
        protected = {"id", "created_at", "updated_at"}
        for k, v in data.items():
            if k in protected:
                continue
            if hasattr(self, k):
                setattr(self, k, v)

        self.validate()
        self.save()