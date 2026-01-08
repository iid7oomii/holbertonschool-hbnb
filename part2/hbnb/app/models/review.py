from __future__ import annotations

from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.user import User
from hbnb.app.models.place import Place


class Review(BaseModel):
    """
    Review entity:
    - text   (required)
    - rating (int 1..5)
    - user   (User instance)
    - place  (Place instance)
    """

    def __init__(
        self,
        text: str,
        rating: int,
        user: User,
        place: Place,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

        self.validate()

        # optional but helpful: auto-link to place
        self.place.add_review(self)

    def validate(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text is required")

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")

        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")