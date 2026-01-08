


from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


class BaseModel:
    """
    Base model providing:
    - id (UUID string)
    - created_at (UTC datetime)
    - updated_at (UTC datetime)
    - save(): updates updated_at
    - update(data): set attributes then validate
    """

    def __init__(self, **kwargs: Any):
        now = datetime.now(timezone.utc)

        self.id: str = kwargs.get("id", str(uuid.uuid4()))
        self.created_at: datetime = kwargs.get("created_at", now)
        self.updated_at: datetime = kwargs.get("updated_at", now)

    def save(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

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